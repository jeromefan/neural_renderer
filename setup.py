from setuptools import setup, find_packages
from torch.utils.cpp_extension import BuildExtension, CUDAExtension


ext_modules = [
    CUDAExtension(
        name="neural_renderer.cuda.load_textures",
        sources=[
            "neural_renderer/cuda/load_textures_cuda.cpp",
            "neural_renderer/cuda/load_textures_cuda_kernel.cu",
        ],
        # include_dirs=["/usr/local/cuda-11.6/include"],
    ),
    CUDAExtension(
        name="neural_renderer.cuda.rasterize",
        sources=[
            "neural_renderer/cuda/rasterize_cuda.cpp",
            "neural_renderer/cuda/rasterize_cuda_kernel.cu",
        ],
        # include_dirs=["/usr/local/cuda-11.6/include"],
    ),
    CUDAExtension(
        name="neural_renderer.cuda.create_texture_image",
        sources=[
            "neural_renderer/cuda/create_texture_image_cuda.cpp",
            "neural_renderer/cuda/create_texture_image_cuda_kernel.cu",
        ],
        # include_dirs=["/usr/local/cuda-11.6/include"],
    ),
]

setup(
    description='PyTorch implementation of "A 3D mesh renderer for neural networks"',
    author='Nikolaos Kolotouros',
    author_email='nkolot@seas.upenn.edu',
    license='MIT License',
    version='1.1.3',
    name='neural_renderer_pytorch',
    packages=['neural_renderer', 'neural_renderer.cuda'],
    ext_modules=ext_modules,
    # cmdclass={'build_ext': BuildExtension},
    cmdclass={"build_ext": BuildExtension.with_options(use_ninja=False)},
)
