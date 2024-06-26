from __future__ import division

import torch


def projection(vertices, K, R, t, dist_coeffs, eps=1e-9):
    """
    Calculate projective transformation of vertices given a projection matrix
    给定投影矩阵，计算顶点的投影变换
    Input parameters:
    K: batch_size * 3 * 3 intrinsic camera matrix
    R, t: batch_size * 3 * 3, batch_size * 1 * 3 extrinsic calibration parameters
    dist_coeffs: vector of distortion coefficients
    orig_size: original size of image captured by the camera
    Returns: For each point [X,Y,Z] in world coordinates [u,v,z] where u,v are the coordinates of the projection in
    pixels and z is the depth
    Returns: 对于世界坐标的每个点[X,Y,Z]，有[u,v,z]，其中u和v为NDC坐标系、z为深度
    """

    # instead of P*x we compute x'*P'
    # 首先使用相机外参将世界坐标的点转换到相机坐标系中
    vertices = torch.matmul(vertices, R.transpose(2, 1)) + t
    x, y, z = vertices[:, :, 0], vertices[:, :, 1], vertices[:, :, 2]
    x_ = x / (z + eps)
    y_ = y / (z + eps)

    # Get distortion coefficients from vector
    k1 = dist_coeffs[:, None, 0]
    k2 = dist_coeffs[:, None, 1]
    p1 = dist_coeffs[:, None, 2]
    p2 = dist_coeffs[:, None, 3]
    k3 = dist_coeffs[:, None, 4]

    # we use x_ for x' and x__ for x'' etc.
    r = torch.sqrt(x_**2 + y_**2)
    x__ = (
        x_ * (1 + k1 * (r**2) + k2 * (r**4) + k3 * (r**6))
        + 2 * p1 * x_ * y_
        + p2 * (r**2 + 2 * x_**2)
    )
    y__ = (
        y_ * (1 + k1 * (r**2) + k2 * (r**4) + k3 * (r**6))
        + p1 * (r**2 + 2 * y_**2)
        + 2 * p2 * x_ * y_
    )
    vertices = torch.stack([x__, y__, torch.ones_like(z)], dim=-1)
    vertices = torch.matmul(vertices, K.transpose(1, 2))
    u, v = vertices[:, :, 0], vertices[:, :, 1]

    # map u,v from [0, img_size] to [-1, 1] to use by the renderer
    w, h = K[0, 0, 2] * 2, K[0, 1, 2] * 2
    u = 2 * (u - w / 2.0) / w
    v = 2 * (v - h / 2.0) / h
    vertices = torch.stack([u, v, z], dim=-1)
    return vertices
