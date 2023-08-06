import onnx
import struct
import torch
import torch.nn as nn
import warnings

import numpy as np

from typing import Optional

# TODO more types maybe?
data_type_tab = {
    1: ['f', 4],
    2: ['B', 1],
    3: ['b', 1],
    4: ['H', 2],
    5: ['h', 2],
    6: ['i', 4],
    7: ['q', 8],
    10: ['e', 2],
    11: ['d', 8],
    12: ['I', 4],
    13: ['Q', 8]
}


def empty(x):
    return x


# TODO pytorch only accepts 2-value list for padding.
def _slim422(l4):
    assert len(l4) == 4

    p0, p1 = l4[::2]
    if l4[0] == 0:  # TODO bad code
        p0 = l4[2] // 2
        if l4[2] == 1:
            p0 = 1
    if l4[1] == 0:  # TODO bad code
        p1 = l4[3] // 2
        if l4[3] == 1:
            p1 = 1
    return p0, p1


def _check_attr(attrs, map):
    for attr in attrs:
        if attr.name not in map:
            warnings.warn("Missing {} in parser's attr_map.".format(attr.name))


def unpack_weights(initializer):
    ret = {}
    for i in initializer:
        name = i.name
        dtype = i.data_type
        shape = list(i.dims)
        if dtype not in data_type_tab:
            warnings("This data type {} is not supported yet.".format(dtype))
        fmt, size = data_type_tab[dtype]
        if len(i.raw_data) == 0:
            if dtype == 1:
                data_list = i.float_data
            elif dtype == 7:
                data_list = i.int64_data
            else:
                warnings.warn("No-raw-data type {} not supported yet.".format(dtype))
        else:
            data_list = struct.unpack('<' + fmt * (len(i.raw_data) // size), i.raw_data)
        t = torch.tensor(data_list)
        if len(shape) != 0:
            t = t.view(*shape)
        ret[name] = t
    return ret


def rebuild_lrn(node, weights):
    # size, alpha = 1e-4, beta = 0.75, k = 1.
    rebuild_lrn.lrn_attr_map = {
        'size': 'size',
        'alpha': 'alpha',
        'beta': 'beta',
        'bias': 'k'
    }
    kwargs = {}
    for att in node.attribute:
        kwargs[rebuild_lrn.lrn_attr_map[att.name]] = att.f if att.name != 'size' else att.i
    return nn.LocalResponseNorm(**kwargs), node.input, node.output


def rebuild_conv(node, weights):
    rebuild_conv.conv_attr_map = {
        "pads": "padding",
        "strides": "stride",
        "kernel_shape": "kernel_size",
        "group": "groups",
        "dilations": "dilation"
    }
    assert len(node.output) == 1
    with_bias = False
    if len(node.input) == 3:
        with_bias = True
        bias_name = node.input[2]
        bias = weights[bias_name]

    weight_name = node.input[1]
    weight = weights[weight_name]
    in_channels = weight.shape[1]
    out_channels = weight.shape[0]
    kwargs = {}
    for att in node.attribute:
        if(att.name not in rebuild_conv.conv_attr_map):
            print(f"{att.name} is not defined in attr_map, skip it")
            continue
        kwargs[rebuild_conv.conv_attr_map[att.name]] = list(att.ints) if att.name != 'group' else att.i
    if 'padding' in kwargs:
        kwargs["padding"] = _slim422(kwargs["padding"])
    groups = 1 if 'groups' not in kwargs else kwargs['groups']
    in_channels *= groups
    conv = nn.Conv2d(in_channels, out_channels, **kwargs, bias=with_bias)
    conv.weight.data = weight
    if with_bias:
        conv.bias.data = bias
    return conv, node.input[:1], node.output


def rebuild_dropout(node, weights):
    ratio = node.attribute[0].f
    return nn.Dropout2d(p=ratio), node.input, node.output


def rebuild_batchnormalization(node, weights):
    rebuild_batchnormalization.bn_attr_map = {
        "epsilon": "eps",
        "momentum": "momentum"
    }
    assert len(node.input) == 5
    assert len(node.output) == 1
    weight = weights[node.input[1]]
    bias = weights[node.input[2]]
    running_mean = weights[node.input[3]]
    running_var = weights[node.input[4]]
    dim = weight.shape[0]
    kwargs = {}
    _check_attr(node.attribute, rebuild_batchnormalization.bn_attr_map)
    for att in node.attribute:
        if att.name in rebuild_batchnormalization.bn_attr_map:
            kwargs[rebuild_batchnormalization.bn_attr_map[att.name]] = att.f

    bn = nn.BatchNorm2d(num_features=dim)
    bn.weight.data = weight
    bn.bias.data = bias
    bn.running_mean.data = running_mean
    bn.running_var.data = running_var
    return bn, node.input[:1], node.output


def rebuild_relu(node, weights):
    return nn.ReLU(), node.input, node.output


def rebuild_maxpool(node, weights):
    # MaxPool 2D only
    # TODO: support ND pooling
    rebuild_maxpool.mp_attr_map = {
        "strides": "stride",
        "kernel_shape": "kernel_size",
    }
    kwargs = {}
    with_padding = False
    for att in node.attribute:
        if(att.name == 'pads'):
            pad_list = list(att.ints)
            pad_list = (pad_list[0], pad_list[2], pad_list[1], pad_list[3])
            pad_layer = nn.ConstantPad2d(pad_list, 0)
            with_padding = True
        else:
            kwargs[rebuild_maxpool.mp_attr_map[att.name]] = list(att.ints)

    if(with_padding):
        mp = nn.Sequential(pad_layer, nn.MaxPool2d(**kwargs))
    else:
        mp = nn.MaxPool2d(**kwargs)

    return mp, node.input, node.output


def rebuild_add(node, weights):
    def add(a, b):
        return a + b
    return add, node.input, node.output


def rebuild_globalaveragepool(node, weights):
    avg_pool = nn.AdaptiveAvgPool2d((1, 1))
    return avg_pool, node.input, node.output


def rebuild_transpose(node, weights):
    perm = node.attribute[0].ints

    def transpose(x):
        x = x.permute(*perm)
        return x
    return transpose, node.input, node.output


def rebuild_flatten(node, weights):
    if len(node.attribute) == 0:
        d = 1
    else:
        d = node.attribute[0].i

    def flatten(x):
        o_shape = []
        for i in range(d):
            o_shape.append(x.shape[i])
        o_shape.append(-1)
        return x.view(*o_shape)
    return flatten, node.input, node.output


def rebuild_gemm(node, weights):
    weight = weights[node.input[1]]
    bias = weights[node.input[2]]
    in_feats = weight.shape[1]
    out_feats = weight.shape[0]
    linear = nn.Linear(in_features=in_feats, out_features=out_feats)
    linear.weight.data = weight
    linear.bias.data = bias
    return linear, node.input[:1], node.output


def rebuild_concat(node, weights):
    dim = node.attribute[0].i

    def concat(*inputs):
        ret = torch.cat(inputs, dim)
        return ret
    return concat, node.input, node.output


def rebuild_pad(node, weights):
    mode = node.attribute[0].s
    pads = list(node.attribute[1].ints)
    value = node.attribute[2].f
    assert mode == b'constant'  # TODO constant only
    assert sum(pads[:4]) == 0  # TODO pad2d only
    pad = nn.ConstantPad2d(pads[4:], value)
    return pad, node.input, node.output


def rebuild_constant(node, weights):
    raw_data = node.attribute[0].t.raw_data
    data_type = node.attribute[0].t.data_type
    fmt, size = data_type_tab[data_type]
    data = struct.unpack('<' + fmt * (len(raw_data) // size), raw_data)
    if len(data) == 1:
        data = data[0]

    def constant():
        return torch.tensor(data)
    return constant, [], node.output


def rebuild_sum(node, weights):
    def sum(*inputs):
        ret = inputs[0]
        for i in inputs[1:]:
            ret += i
        return ret
    return sum, node.input, node.output


def rebuild_reducemean(node, weights):
    kwargs = {}
    for att in node.attribute:
        if(att.name == 'axes'):
            kwargs['dim'] = tuple(att.ints)
        if(att.name == 'keepdims'):
            kwargs['keepdim'] = bool(att.i)

    def reduce_mean(x):
        return torch.mean(x, **kwargs)

    return reduce_mean, node.input, node.output


def rebuild_shape(node, weights):
    def shape(x):
        return torch.tensor(list(x.shape))
    return shape, node.input, node.output


def rebuild_gather(node, weights):
    axis = node.attribute[0].i

    def gather(x, idx):
        return torch.gather(x, axis, idx)
    return gather, node.input, node.output


def _nd_unsqueeze(x, dims):
    dims = sorted(dims)
    for d in dims:
        x = torch.unsqueeze(x, dim=d)
    return x


def rebuild_unsqueeze(node, weights):
    axes = node.attribute[0].ints

    def unsqueeze(x):
        return _nd_unsqueeze(x, axes)

    return unsqueeze, node.input, node.output


def _nd_squeeze(x, dims):
    dims = sorted(dims)
    dims = dims[::-1]
    for d in dims:
        x = torch.squeeze(x, dim=d)
    return x


def rebuild_squeeze(node, weights):
    axes = node.attribute[0].ints

    def squeeze(x):
        return _nd_squeeze(x, axes)

    return squeeze, node.input, node.output


def rebuild_mul(node, weights):
    def mul(a, b):
        return a * b
    return mul, node.input, node.output


def rebuild_softmax(node, weights):
    def f_softmax(x):
        return x.softmax(dim=1, dtype=torch.double).float()
    return f_softmax, node.input, node.output


def rebuild_reshape(node, weights):
    def reshape(x, s):
        data_shape = x.shape
        onnx_shape = s.tolist()
        pt_shape = []
        for idx, d in enumerate(onnx_shape):
            if d == 0:
                pt_shape.append(data_shape[idx])
            else:
                pt_shape.append(d)
        return torch.reshape(x, pt_shape)
    return reshape, node.input, node.output


def rebuild_averagepool(node, weights):
    rebuild_averagepool.avg_attr_map = {
        "pads": "padding",
        "strides": "stride",
        "kernel_shape": "kernel_size",
    }
    kwargs = {}

    for att in node.attribute:
        kwargs[rebuild_averagepool.avg_attr_map[att.name]] = list(att.ints)
    if 'padding' in kwargs:
        kwargs["padding"] = _slim422(kwargs["padding"])
    ap = nn.AvgPool2d(**kwargs)
    return ap, node.input, node.output


def rebuild_op(node, weights):
    op_type = node.op_type
    return globals()['rebuild_' + op_type.lower()](node, weights)


def construct_pytorch_nodes(graph, weights):
    ret = []
    for single_node in graph.node:
        ret.append(rebuild_op(single_node, weights))
    return ret


def resolve_deps(name, deps, inter_tensors):
    if name in inter_tensors:
        return
    else:
        op, deps_names = deps[name]
        args = []
        args_name_list = []
        for deps_name in deps_names:
            resolve_deps(deps_name, deps, inter_tensors)
            args.append(inter_tensors[deps_name])
            args_name_list.append(deps_name)
        result = op(*args)
        inter_tensors[name] = result


def testOnnxPyTorch(onnx_model: str):
    import onnxruntime as nxrun
    reconstruct_model = ONNXPytorchModule(onnx_model)
    reconstruct_model.eval()

    img_tensor = torch.randn(1, 3, 224, 224)
    img = img_tensor.cpu().numpy()
    result_pt = reconstruct_model(img_tensor).detach().cpu().numpy()

    sess = nxrun.InferenceSession(onnx_model)
    input_name = sess.get_inputs()[0].name
    result = sess.run(None, {input_name: img})
    result_onnx = result[0]

    print(f"Max error = {np.max(np.abs(result_onnx - result_pt))}")
    print(f"average error = {np.mean(np.abs(result_onnx - result_pt))}")


class ONNXPytorchModule(nn.Module):
    '''
    A Pytorch Module with onnx weights.
    Ref and fix some bugs from https://gist.github.com/qinjian623/6aa777037534c1c1dccbb66f832e93b8
    '''
    def __init__(self, onnx_model: str, input_name: Optional[str] = None):
        super(ONNXPytorchModule, self).__init__()
        onnx_model = onnx.load(onnx_model)
        weights = unpack_weights(onnx_model.graph.initializer)
        nodes = construct_pytorch_nodes(onnx_model.graph, weights)

        self.inter_tensors = dict()
        self.deps = dict()
        for idx, (node, inputs, outputs) in enumerate(nodes):
            if isinstance(node, nn.Module):
                self.add_module(str(idx), node)
            for output_name in outputs:
                self.deps[output_name] = (node, inputs)

        self.input_name = onnx_model.graph.input[0].name
        self.output_name = onnx_model.graph.output[0].name
        if input_name is not None:
            self.input_name = input_name

    def forward(self, input):
        self.inter_tensors.clear()
        self.inter_tensors[self.input_name] = input
        resolve_deps(self.output_name, self.deps, self.inter_tensors)
        return self.inter_tensors[self.output_name]