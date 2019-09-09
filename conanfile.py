from conans import ConanFile, CMake, tools
import sys
import os


class LibtorchConan(ConanFile):
    name = "libtorch"
    version = "1.2.0"
    license = "Pytorch"
    author = ""
    url = "<Package recipe repository url here, for issues about the package>"
    description = "An open source machine learning framework that accelerates the path from research prototyping to production deployment."
    topics = ("pytorch", "torch", "libtorch", "machine learning", "neural networks")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": True}
    generators = ["cmake"]

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def requirements(self):
        self.requires("eigen/3.3.7@conan/stable")
        self.requires("pybind11/2.2.4@conan/stable")
        self.requires("openblas/0.3.5@conan/stable")
        self.requires("protobuf/3.6.1@bincrafters/stable")

    def source(self):
        git = tools.Git(folder="source_subfolder")
        git.clone("https://github.com/pytorch/pytorch.git", "v{}".format(self.version), shallow=True)

        #Clone only the required submodules
        self.run("cd source_subfolder && git submodule update --init third_party/cpuinfo")
        self.run("cd source_subfolder && git submodule update --init third_party/FP16")
        self.run("cd source_subfolder && git submodule update --init third_party/onnx")
        self.run("cd source_subfolder && git submodule update --init third_party/foxi")
        self.run("cd source_subfolder && git submodule update --init third_party/sleef")
        #self.run("cd source_subfolder && git submodule update --init third_party/protobuf")


    def _configure_cmake(self):
        cmake = CMake(self)

        cmake.definitions["PYTHON_EXECUTABLE"] = sys.executable
        cmake.definitions["ATEN_NO_TEST"] = True

        cmake.definitions["BUILD_BINARY"] = False
        cmake.definitions["BUILD_PYTHON"] = False
        cmake.definitions["BUILD_CAFFE2_MOBILE"]=False
        cmake.definitions["BUILD_TEST"] = False
        cmake.definitions["BUILD_CUSTOM_PROTOBUF"] = False
        cmake.definitions["BUILD_DOCS"] = False
        cmake.definitions["BUILD_CAFFE2_OPS"] = True
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["BUILD_NAMEDTENSOR"] = False

        cmake.definitions["USE_ASAN"] = False
        cmake.definitions["USE_TBB"] = False
        cmake.definitions["USE_QNNPACK"] = False
        cmake.definitions["USE_NNPACK"] = False
        cmake.definitions["USE_GFLAGS"] = False # It is strongly recommended that this be active
        cmake.definitions["USE_GLOG"] = False # It is strongly recommended that this be active
        cmake.definitions["USE_FBGEMM"] = False
        cmake.definitions["USE_LMDB"] = False
        cmake.definitions["USE_OPENCL"] = False
        cmake.definitions["USE_LEVELDB"] = False
        cmake.definitions["USE_NUMA"] = False
        cmake.definitions["USE_ZMQ"] = False
        cmake.definitions["USE_REDIS"] = False
        cmake.definitions["USE_OPENCV"] = False
        cmake.definitions["USE_FFMPEG"] = False
        cmake.definitions["USE_OPENMP"] = False
        cmake.definitions["USE_CUDA"] = False
        cmake.definitions["USE_CUDNN"] = False
        cmake.definitions["USE_NVRTC"] = False
        cmake.definitions["USE_TENSORRT"] = False
        cmake.definitions["USE_ROCM"] = False
        cmake.definitions["USE_NCCL"] = False
        cmake.definitions["USE_SYSTEM_NCCL"] = False
        cmake.definitions["USE_DISTRIBUTED"] = False
        cmake.definitions["USE_MPI"] = False
        cmake.definitions["USE_GLOO"] = False
        cmake.definitions["USE_PROF"] = False
        cmake.definitions["USE_SNPE"] = False
        cmake.definitions["USE_METAL"] = False
        cmake.definitions["USE_NNAPI"] = False
        cmake.definitions["USE_ZSTD"] = False
        cmake.definitions["USE_MKLDNN"] = False
        cmake.definitions["USE_NUMPY"] = False
        cmake.definitions["USE_SYSTEM_EIGEN_INSTALL"] = True

        cmake.definitions["BLAS"] = "OpenBLAS"
        cmake.definitions["BLAS_SET_BY_USER"] = True

        cmake.configure(build_folder=self._build_subfolder, source_folder=self._source_subfolder)
        return cmake


    def build(self):
        tools.replace_in_file("source_subfolder/CMakeLists.txt", "project(Caffe2 CXX C)", 'project(Caffe2 CXX C)\ninclude("${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake")\nconan_basic_setup()')
        cmake = self._configure_cmake()
        cmake.build()


    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()


    def package_info(self):
        self.cpp_info.libs = ['torch', 'c10']
        self.cpp_info.includedirs = ['include', 'include/torch/csrc/api/include']
