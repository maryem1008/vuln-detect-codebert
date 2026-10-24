# RUNLOG — vuln-detect-codebert

- Start: 2026-10-24T20:04:14+00:00
- Fresh build from CodeBERT_Vuln_Detection_Full_Spec_v2.docx.
- Dataset acquisition authorized by operator: Kaggle token is present.

## A. Environment setup
- Command: python3 -m venv .venv
Python 3.12.3
Requirement already satisfied: pip in ./.venv/lib/python3.12/site-packages (24.0)
Collecting pip
  Downloading pip-26.2.2-py3-none-any.whl.metadata (4.6 kB)
Downloading pip-26.2.2-py3-none-any.whl (1.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 17.0 MB/s eta 0:00:00
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 24.0
    Uninstalling pip-24.0:
      Successfully uninstalled pip-24.0
Successfully installed pip-26.2.2
Collecting transformers
  Downloading transformers-5.20.2-py3-none-any.whl.metadata (31 kB)
Collecting datasets
  Downloading datasets-5.1.0-py3-none-any.whl.metadata (24 kB)
Collecting torch
  Downloading torch-2.14.1-cp312-cp312-manylinux_2_28_x86_64.whl.metadata (37 kB)
Collecting scikit-learn
  Downloading scikit_learn-1.9.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (9.3 kB)
Collecting xgboost
  Downloading xgboost-3.4.1-py3-none-manylinux_2_28_x86_64.whl.metadata (2.0 kB)
Collecting pandas
  Downloading pandas-3.1.0-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.metadata (18 kB)
Collecting numpy
  Downloading numpy-2.5.4-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (6.6 kB)
Collecting tqdm
  Downloading tqdm-4.70.1-py3-none-any.whl.metadata (57 kB)
Collecting matplotlib
  Downloading matplotlib-3.11.2-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (80 kB)
Collecting captum
  Downloading captum-0.9.0-py3-none-any.whl.metadata (24 kB)
Collecting kaggle
  Downloading kaggle-2.2.5-py3-none-any.whl.metadata (17 kB)
Collecting fastapi
  Downloading fastapi-0.162.0-py3-none-any.whl.metadata (26 kB)
Collecting python-multipart
  Downloading python_multipart-0.0.32-py3-none-any.whl.metadata (2.1 kB)
Collecting jinja2
  Downloading jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)
Collecting uvicorn[standard]
  Downloading uvicorn-0.54.0-py3-none-any.whl.metadata (6.6 kB)
Collecting huggingface-hub<3.0,>=1.31.0 (from transformers)
  Downloading huggingface_hub-2.3.0-py3-none-any.whl.metadata (16 kB)
Collecting packaging>=20.0 (from transformers)
  Downloading packaging-26.3-py3-none-any.whl.metadata (3.5 kB)
Collecting pyyaml>=5.1 (from transformers)
  Downloading pyyaml-6.0.3-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.4 kB)
Collecting regex>=2025.10.22 (from transformers)
  Downloading regex-2026.9.29-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (40 kB)
Collecting tokenizers<0.24.0,>=0.23.1 (from transformers)
  Downloading tokenizers-0.23.3-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (9.8 kB)
Collecting typer (from transformers)
  Downloading typer-0.27.3-py3-none-any.whl.metadata (16 kB)
Collecting safetensors>=0.8.0 (from transformers)
  Downloading safetensors-0.8.0-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.2 kB)
Collecting click<9.0.0,>=8.4.2 (from huggingface-hub<3.0,>=1.31.0->transformers)
  Downloading click-8.5.0-py3-none-any.whl.metadata (2.6 kB)
Collecting filelock>=3.10.0 (from huggingface-hub<3.0,>=1.31.0->transformers)
  Downloading filelock-4.2.4-py3-none-any.whl.metadata (2.0 kB)
Collecting fsspec>=2023.5.0 (from huggingface-hub<3.0,>=1.31.0->transformers)
  Downloading fsspec-2026.9.0-py3-none-any.whl.metadata (10 kB)
Collecting hf-xet<2.0.0,>=1.6.0 (from huggingface-hub<3.0,>=1.31.0->transformers)
  Downloading hf_xet-1.7.0-cp38-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (4.9 kB)
Collecting httpx2<3,>=2.0.0 (from huggingface-hub<3.0,>=1.31.0->transformers)
  Downloading httpx2-2.16.0-py3-none-any.whl.metadata (10 kB)
Collecting typing-extensions>=4.1.0 (from huggingface-hub<3.0,>=1.31.0->transformers)
  Downloading typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
Collecting anyio>=4.10 (from httpx2<3,>=2.0.0->huggingface-hub<3.0,>=1.31.0->transformers)
  Downloading anyio-4.15.1-py3-none-any.whl.metadata (4.7 kB)
Collecting httpcore2==2.16.0 (from httpx2<3,>=2.0.0->huggingface-hub<3.0,>=1.31.0->transformers)
  Downloading httpcore2-2.16.0-py3-none-any.whl.metadata (27 kB)
Collecting idna>=3.18 (from httpx2<3,>=2.0.0->huggingface-hub<3.0,>=1.31.0->transformers)
  Downloading idna-3.20-py3-none-any.whl.metadata (7.2 kB)
Collecting truststore>=0.10 (from httpx2<3,>=2.0.0->huggingface-hub<3.0,>=1.31.0->transformers)
  Downloading truststore-0.10.5-py3-none-any.whl.metadata (4.5 kB)
Collecting h11>=0.16 (from httpcore2==2.16.0->httpx2<3,>=2.0.0->huggingface-hub<3.0,>=1.31.0->transformers)
  Downloading h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
Collecting pyarrow>=24.0.0 (from datasets)
  Downloading pyarrow-26.0.0-cp312-cp312-manylinux_2_28_x86_64.whl.metadata (3.0 kB)
Collecting dill<0.4.2,>=0.3.0 (from datasets)
  Downloading dill-0.4.1-py3-none-any.whl.metadata (10 kB)
Collecting xxhash (from datasets)
  Downloading xxhash-4.0.2-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (17 kB)
Collecting multiprocess<0.70.20 (from datasets)
  Downloading multiprocess-0.70.19-py312-none-any.whl.metadata (7.5 kB)
Collecting fsspec>=2023.5.0 (from huggingface-hub<3.0,>=1.31.0->transformers)
  Downloading fsspec-2026.7.0-py3-none-any.whl.metadata (10 kB)
Collecting aiohttp!=4.0.0a0,!=4.0.0a1 (from fsspec[http]<=2026.7.0,>=2023.1.0->datasets)
  Downloading aiohttp-3.14.5-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (8.3 kB)
Collecting setuptools>=77.0.3 (from torch)
  Downloading setuptools-84.2.1-py3-none-any.whl.metadata (6.6 kB)
Collecting sympy>=1.13.3 (from torch)
  Downloading sympy-1.14.0-py3-none-any.whl.metadata (12 kB)
Collecting networkx>=2.5.1 (from torch)
  Downloading networkx-3.7-py3-none-any.whl.metadata (6.7 kB)
Collecting cuda-toolkit==13.0.3 (from cuda-toolkit[cublas,cudart,cufft,cufile,cupti,curand,cusolver,cusparse,nvjitlink,nvrtc,nvtx]==13.0.3; platform_system == "Linux"->torch)
  Downloading cuda_toolkit-13.0.3.0-py2.py3-none-any.whl.metadata (17 kB)
Collecting cuda-bindings<14,>=13.0.3 (from torch)
  Downloading cuda_bindings-13.4.4-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.metadata (2.4 kB)
Collecting nvidia-cudnn-cu13==9.24.0.43 (from torch)
  Downloading nvidia_cudnn_cu13-9.24.0.43-py3-none-manylinux_2_27_x86_64.whl.metadata (1.9 kB)
Collecting nvidia-cusparselt-cu13==0.8.1 (from torch)
  Downloading nvidia_cusparselt_cu13-0.8.1-py3-none-manylinux2014_x86_64.whl.metadata (12 kB)
Collecting nvidia-nccl-cu13==2.30.7 (from torch)
  Downloading nvidia_nccl_cu13-2.30.7-py3-none-manylinux_2_18_x86_64.whl.metadata (2.1 kB)
Collecting nvidia-nvshmem-cu13==3.4.5 (from torch)
  Downloading nvidia_nvshmem_cu13-3.4.5-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (2.1 kB)
Collecting triton~=3.8.0 (from torch)
  Downloading triton-3.8.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (978 bytes)
Collecting nvidia-cublas==13.1.1.3.* (from cuda-toolkit[cublas,cudart,cufft,cufile,cupti,curand,cusolver,cusparse,nvjitlink,nvrtc,nvtx]==13.0.3; platform_system == "Linux"->torch)
  Downloading nvidia_cublas-13.1.1.3-py3-none-manylinux_2_27_x86_64.whl.metadata (1.8 kB)
Collecting nvidia-cuda-nvrtc==13.0.88.* (from cuda-toolkit[cublas,cudart,cufft,cufile,cupti,curand,cusolver,cusparse,nvjitlink,nvrtc,nvtx]==13.0.3; platform_system == "Linux"->torch)
  Downloading nvidia_cuda_nvrtc-13.0.88-py3-none-manylinux2010_x86_64.manylinux_2_12_x86_64.whl.metadata (1.7 kB)
Collecting nvidia-cuda-runtime==13.0.96.* (from cuda-toolkit[cublas,cudart,cufft,cufile,cupti,curand,cusolver,cusparse,nvjitlink,nvrtc,nvtx]==13.0.3; platform_system == "Linux"->torch)
  Downloading nvidia_cuda_runtime-13.0.96-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (1.7 kB)
Collecting nvidia-cufft==12.0.0.61.* (from cuda-toolkit[cublas,cudart,cufft,cufile,cupti,curand,cusolver,cusparse,nvjitlink,nvrtc,nvtx]==13.0.3; platform_system == "Linux"->torch)
  Downloading nvidia_cufft-12.0.0.61-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (1.8 kB)
Collecting nvidia-nvjitlink<14,>=13.0.88 (from cuda-toolkit[cublas,cudart,cufft,cufile,cupti,curand,cusolver,cusparse,nvjitlink,nvrtc,nvtx]==13.0.3; platform_system == "Linux"->torch)
  Downloading nvidia_nvjitlink-13.4.92-py3-none-manylinux2010_x86_64.manylinux_2_12_x86_64.whl.metadata (1.8 kB)
Collecting nvidia-cufile==1.15.1.6.* (from cuda-toolkit[cublas,cudart,cufft,cufile,cupti,curand,cusolver,cusparse,nvjitlink,nvrtc,nvtx]==13.0.3; platform_system == "Linux"->torch)
  Downloading nvidia_cufile-1.15.1.6-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (1.7 kB)
Collecting nvidia-cuda-cupti==13.0.85.* (from cuda-toolkit[cublas,cudart,cufft,cufile,cupti,curand,cusolver,cusparse,nvjitlink,nvrtc,nvtx]==13.0.3; platform_system == "Linux"->torch)
  Downloading nvidia_cuda_cupti-13.0.85-py3-none-manylinux_2_25_x86_64.whl.metadata (1.7 kB)
Collecting nvidia-curand==10.4.0.35.* (from cuda-toolkit[cublas,cudart,cufft,cufile,cupti,curand,cusolver,cusparse,nvjitlink,nvrtc,nvtx]==13.0.3; platform_system == "Linux"->torch)
  Downloading nvidia_curand-10.4.0.35-py3-none-manylinux_2_27_x86_64.whl.metadata (1.7 kB)
Collecting nvidia-cusolver==12.0.4.66.* (from cuda-toolkit[cublas,cudart,cufft,cufile,cupti,curand,cusolver,cusparse,nvjitlink,nvrtc,nvtx]==13.0.3; platform_system == "Linux"->torch)
  Downloading nvidia_cusolver-12.0.4.66-py3-none-manylinux_2_27_x86_64.whl.metadata (1.8 kB)
Collecting nvidia-cusparse==12.6.3.3.* (from cuda-toolkit[cublas,cudart,cufft,cufile,cupti,curand,cusolver,cusparse,nvjitlink,nvrtc,nvtx]==13.0.3; platform_system == "Linux"->torch)
  Downloading nvidia_cusparse-12.6.3.3-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (1.8 kB)
Collecting nvidia-nvtx==13.0.85.* (from cuda-toolkit[cublas,cudart,cufft,cufile,cupti,curand,cusolver,cusparse,nvjitlink,nvrtc,nvtx]==13.0.3; platform_system == "Linux"->torch)
  Downloading nvidia_nvtx-13.0.85-py3-none-manylinux1_x86_64.manylinux_2_5_x86_64.whl.metadata (1.8 kB)
Collecting cuda-pathfinder>=1.4.2 (from cuda-bindings<14,>=13.0.3->torch)
  Downloading cuda_pathfinder-1.8.4-py3-none-any.whl.metadata (1.9 kB)
Collecting scipy>=1.10.0 (from scikit-learn)
  Downloading scipy-1.18.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (62 kB)
Collecting joblib>=1.4.0 (from scikit-learn)
  Downloading joblib-1.6.0-py3-none-any.whl.metadata (6.5 kB)
Collecting narwhals>=2.0.1 (from scikit-learn)
  Downloading narwhals-2.27.1-py3-none-any.whl.metadata (15 kB)
Collecting threadpoolctl>=3.5.0 (from scikit-learn)
  Downloading threadpoolctl-3.7.0-py3-none-any.whl.metadata (24 kB)
Collecting python-dateutil>=2.9.0 (from pandas)
  Downloading python_dateutil-3.0.0-py2.py3-none-any.whl.metadata (8.2 kB)
Collecting contourpy>=1.0.1 (from matplotlib)
  Downloading contourpy-1.4.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (3.8 kB)
Collecting cycler>=0.10 (from matplotlib)
  Downloading cycler-0.12.1-py3-none-any.whl.metadata (3.8 kB)
Collecting fonttools>=4.28.2 (from matplotlib)
  Downloading fonttools-4.67.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (137 kB)
Collecting kiwisolver>=1.3.1 (from matplotlib)
  Downloading kiwisolver-1.5.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (5.2 kB)
Collecting pillow>=9 (from matplotlib)
  Downloading pillow-13.0.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (9.1 kB)
Collecting pyparsing>=3 (from matplotlib)
  Downloading pyparsing-3.3.3-py3-none-any.whl.metadata (5.9 kB)
Collecting bleach (from kaggle)
  Downloading bleach-6.4.0-py3-none-any.whl.metadata (32 kB)
Collecting certifi>=2026.10.19 (from kaggle)
  Downloading certifi-2026.10.23-py3-none-any.whl.metadata (2.5 kB)
Collecting jupytext (from kaggle)
  Downloading jupytext-1.19.6-py3-none-any.whl.metadata (15 kB)
Collecting kagglesdk<1.0,>=0.1.38 (from kaggle)
  Downloading kagglesdk-0.1.38-py3-none-any.whl.metadata (13 kB)
Collecting protobuf (from kaggle)
  Downloading protobuf-7.36.2-cp310-abi3-manylinux2014_x86_64.whl.metadata (595 bytes)
Collecting python-dotenv (from kaggle)
  Downloading python_dotenv-1.2.4-py3-none-any.whl.metadata (29 kB)
Collecting python-slugify (from kaggle)
  Downloading python_slugify-9.1.3-py3-none-any.whl.metadata (12 kB)
Collecting requests (from kaggle)
  Downloading requests-2.34.2-py3-none-any.whl.metadata (4.8 kB)
Collecting urllib3>=1.15.1 (from kaggle)
  Downloading urllib3-2.8.0-py3-none-any.whl.metadata (7.4 kB)
Collecting starlette>=0.46.0 (from fastapi)
  Downloading starlette-1.10.0-py3-none-any.whl.metadata (6.6 kB)
Collecting pydantic>=2.9.0 (from fastapi)
  Downloading pydantic-2.14.1-py3-none-any.whl.metadata (133 kB)
Collecting typing-inspection>=0.4.2 (from fastapi)
  Downloading typing_inspection-0.4.4-py3-none-any.whl.metadata (2.6 kB)
Collecting annotated-doc>=0.0.2 (from fastapi)
  Downloading annotated_doc-0.0.5-py3-none-any.whl.metadata (6.5 kB)
Collecting opentelemetry-api>=1.44.0 (from fastapi)
  Downloading opentelemetry_api-1.45.1-py3-none-any.whl.metadata (1.4 kB)
Collecting httptools>=0.8.0 (from uvicorn[standard])
  Downloading httptools-0.9.0-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (3.5 kB)
Collecting uvloop>=0.15.1 (from uvicorn[standard])
  Downloading uvloop-0.23.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (5.1 kB)
Collecting watchfiles>=0.20 (from uvicorn[standard])
  Downloading watchfiles-1.3.0-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.9 kB)
Collecting websockets>=13.0 (from uvicorn[standard])
  Downloading websockets-17.3-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (6.3 kB)
Collecting MarkupSafe>=2.0 (from jinja2)
  Downloading markupsafe-3.0.4-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.7 kB)
Collecting aiohappyeyeballs>=2.5.0 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.7.0,>=2023.1.0->datasets)
  Downloading aiohappyeyeballs-2.7.1-py3-none-any.whl.metadata (5.9 kB)
Collecting aiosignal>=1.4.0 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.7.0,>=2023.1.0->datasets)
  Downloading aiosignal-1.4.0-py3-none-any.whl.metadata (3.7 kB)
Collecting attrs>=17.3.0 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.7.0,>=2023.1.0->datasets)
  Downloading attrs-26.1.0-py3-none-any.whl.metadata (8.8 kB)
Collecting frozenlist>=1.1.1 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.7.0,>=2023.1.0->datasets)
  Downloading frozenlist-1.8.0-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (20 kB)
Collecting multidict<8.0,>=4.5 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.7.0,>=2023.1.0->datasets)
  Downloading multidict-7.2.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (6.1 kB)
Collecting propcache>=0.2.0 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.7.0,>=2023.1.0->datasets)
  Downloading propcache-0.5.4-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (25 kB)
Collecting yarl<2.0,>=1.25.1 (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2026.7.0,>=2023.1.0->datasets)
  Downloading yarl-1.25.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (111 kB)
Collecting cloudpickle>=3.0 (from joblib>=1.4.0->scikit-learn)
  Downloading cloudpickle-3.1.2-py3-none-any.whl.metadata (7.1 kB)
Collecting annotated-types>=0.6.0 (from pydantic>=2.9.0->fastapi)
  Downloading annotated_types-0.8.0-py3-none-any.whl.metadata (15 kB)
Collecting pydantic-core==2.50.1 (from pydantic>=2.9.0->fastapi)
  Downloading pydantic_core-2.50.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.5 kB)
Collecting six>=1.6 (from python-dateutil>=2.9.0->pandas)
  Downloading six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
Collecting tzdata (from python-dateutil>=2.9.0->pandas)
  Downloading tzdata-2026.5-py2.py3-none-any.whl.metadata (1.4 kB)
Collecting mpmath<1.4,>=1.1.0 (from sympy>=1.13.3->torch)
  Downloading mpmath-1.3.0-py3-none-any.whl.metadata (8.6 kB)
Collecting webencodings (from bleach->kaggle)
  Downloading webencodings-0.6.1-py3-none-any.whl.metadata (3.4 kB)
Collecting markdown-it-py>=1.0 (from jupytext->kaggle)
  Downloading markdown_it_py-4.2.0-py3-none-any.whl.metadata (7.4 kB)
Collecting mdit-py-plugins (from jupytext->kaggle)
  Downloading mdit_py_plugins-0.6.1-py3-none-any.whl.metadata (2.9 kB)
Collecting nbformat (from jupytext->kaggle)
  Downloading nbformat-5.11.1-py3-none-any.whl.metadata (3.7 kB)
Collecting mdurl~=0.1 (from markdown-it-py>=1.0->jupytext->kaggle)
  Downloading mdurl-0.1.2-py3-none-any.whl.metadata (1.6 kB)
Collecting fastjsonschema>=2.15 (from nbformat->jupytext->kaggle)
  Downloading fastjsonschema-2.22.2-py3-none-any.whl.metadata (2.1 kB)
Collecting jsonschema>=2.6 (from nbformat->jupytext->kaggle)
  Downloading jsonschema-4.26.0-py3-none-any.whl.metadata (7.6 kB)
Collecting jupyter-core!=5.0.*,>=4.12 (from nbformat->jupytext->kaggle)
  Downloading jupyter_core-5.9.1-py3-none-any.whl.metadata (1.5 kB)
Collecting traitlets>=5.1 (from nbformat->jupytext->kaggle)
  Downloading traitlets-5.16.1-py3-none-any.whl.metadata (10 kB)
Collecting jsonschema-specifications>=2023.03.6 (from jsonschema>=2.6->nbformat->jupytext->kaggle)
  Downloading jsonschema_specifications-2025.9.1-py3-none-any.whl.metadata (2.9 kB)
Collecting referencing>=0.28.4 (from jsonschema>=2.6->nbformat->jupytext->kaggle)
  Downloading referencing-0.37.0-py3-none-any.whl.metadata (2.8 kB)
Collecting rpds-py>=0.25.0 (from jsonschema>=2.6->nbformat->jupytext->kaggle)
  Downloading rpds_py-2026.9.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.1 kB)
Collecting platformdirs>=2.5 (from jupyter-core!=5.0.*,>=4.12->nbformat->jupytext->kaggle)
  Downloading platformdirs-4.13.5-py3-none-any.whl.metadata (5.5 kB)
Collecting text-unidecode>=1.3 (from python-slugify->kaggle)
  Downloading text_unidecode-1.3-py2.py3-none-any.whl.metadata (2.4 kB)
Collecting charset_normalizer<4,>=2 (from requests->kaggle)
  Downloading charset_normalizer-3.5.2-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (46 kB)
Collecting shellingham>=1.3.0 (from typer->transformers)
  Downloading shellingham-1.5.4-py2.py3-none-any.whl.metadata (3.5 kB)
Collecting rich>=13.8.0 (from typer->transformers)
  Downloading rich-15.0.0-py3-none-any.whl.metadata (18 kB)
Collecting pygments<3.0.0,>=2.13.0 (from rich>=13.8.0->typer->transformers)
  Downloading pygments-2.21.0-py3-none-any.whl.metadata (2.5 kB)
Downloading transformers-5.20.2-py3-none-any.whl (12.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.8/12.8 MB 92.7 MB/s  0:00:00
Downloading huggingface_hub-2.3.0-py3-none-any.whl (855 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 855.2/855.2 kB 129.7 MB/s  0:00:00
Downloading click-8.5.0-py3-none-any.whl (125 kB)
Downloading hf_xet-1.7.0-cp38-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (4.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.2/4.2 MB 174.8 MB/s  0:00:00
Downloading httpx2-2.16.0-py3-none-any.whl (97 kB)
Downloading httpcore2-2.16.0-py3-none-any.whl (85 kB)
Downloading tokenizers-0.23.3-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.4/3.4 MB 285.1 MB/s  0:00:00
Downloading datasets-5.1.0-py3-none-any.whl (604 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 604.4/604.4 kB 77.4 MB/s  0:00:00
Downloading dill-0.4.1-py3-none-any.whl (120 kB)
Downloading fsspec-2026.7.0-py3-none-any.whl (206 kB)
Downloading multiprocess-0.70.19-py312-none-any.whl (150 kB)
Downloading torch-2.14.1-cp312-cp312-manylinux_2_28_x86_64.whl (554.6 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 554.6/554.6 MB 115.0 MB/s  0:00:04
Downloading cuda_toolkit-13.0.3.0-py2.py3-none-any.whl (2.5 kB)
Downloading nvidia_cudnn_cu13-9.24.0.43-py3-none-manylinux_2_27_x86_64.whl (553.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 553.1/553.1 MB 91.0 MB/s  0:00:05
Downloading nvidia_cusparselt_cu13-0.8.1-py3-none-manylinux2014_x86_64.whl (170.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 170.1/170.1 MB 111.4 MB/s  0:00:01
Downloading nvidia_nccl_cu13-2.30.7-py3-none-manylinux_2_18_x86_64.whl (216.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 216.0/216.0 MB 100.2 MB/s  0:00:02
Downloading nvidia_nvshmem_cu13-3.4.5-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (60.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 60.4/60.4 MB 219.3 MB/s  0:00:00
Downloading cuda_bindings-13.4.4-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (7.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.2/7.2 MB 114.6 MB/s  0:00:00
Downloading nvidia_cublas-13.1.1.3-py3-none-manylinux_2_27_x86_64.whl (423.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 423.1/423.1 MB 120.6 MB/s  0:00:03
Downloading nvidia_cuda_cupti-13.0.85-py3-none-manylinux_2_25_x86_64.whl (10.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 10.7/10.7 MB 87.8 MB/s  0:00:00
Downloading nvidia_cuda_nvrtc-13.0.88-py3-none-manylinux2010_x86_64.manylinux_2_12_x86_64.whl (90.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 90.2/90.2 MB 130.8 MB/s  0:00:00
Downloading nvidia_cuda_runtime-13.0.96-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (2.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.2/2.2 MB 134.3 MB/s  0:00:00
Downloading nvidia_cufft-12.0.0.61-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (214.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 214.1/214.1 MB 110.6 MB/s  0:00:01
Downloading nvidia_cufile-1.15.1.6-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (1.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 47.3 MB/s  0:00:00
Downloading nvidia_curand-10.4.0.35-py3-none-manylinux_2_27_x86_64.whl (59.5 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 59.5/59.5 MB 113.6 MB/s  0:00:00
Downloading nvidia_cusolver-12.0.4.66-py3-none-manylinux_2_27_x86_64.whl (200.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 200.9/200.9 MB 130.0 MB/s  0:00:01
Downloading nvidia_cusparse-12.6.3.3-py3-none-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (145.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 145.9/145.9 MB 101.4 MB/s  0:00:01
Downloading nvidia_nvjitlink-13.4.92-py3-none-manylinux2010_x86_64.manylinux_2_12_x86_64.whl (42.5 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 42.5/42.5 MB 138.0 MB/s  0:00:00
Downloading nvidia_nvtx-13.0.85-py3-none-manylinux1_x86_64.manylinux_2_5_x86_64.whl (148 kB)
Downloading triton-3.8.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (248.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 248.0/248.0 MB 115.6 MB/s  0:00:02
Downloading scikit_learn-1.9.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (9.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 9.2/9.2 MB 124.4 MB/s  0:00:00
Downloading xgboost-3.4.1-py3-none-manylinux_2_28_x86_64.whl (57.6 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 57.6/57.6 MB 97.1 MB/s  0:00:00
Downloading pandas-3.1.0-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (12.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.0/12.0 MB 285.0 MB/s  0:00:00
Downloading numpy-2.5.4-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.7/16.7 MB 316.2 MB/s  0:00:00
Downloading tqdm-4.70.1-py3-none-any.whl (80 kB)
Downloading matplotlib-3.11.2-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (9.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 9.9/9.9 MB 99.6 MB/s  0:00:00
Downloading captum-0.9.0-py3-none-any.whl (455 kB)
Downloading kaggle-2.2.5-py3-none-any.whl (140 kB)
Downloading kagglesdk-0.1.38-py3-none-any.whl (290 kB)
Downloading fastapi-0.162.0-py3-none-any.whl (148 kB)
Downloading uvicorn-0.54.0-py3-none-any.whl (87 kB)
Downloading python_multipart-0.0.32-py3-none-any.whl (30 kB)
Downloading jinja2-3.1.6-py3-none-any.whl (134 kB)
Downloading aiohttp-3.14.5-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (1.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.9/1.9 MB 232.7 MB/s  0:00:00
Downloading multidict-7.2.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (515 kB)
Downloading yarl-1.25.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (117 kB)
Downloading aiohappyeyeballs-2.7.1-py3-none-any.whl (15 kB)
Downloading aiosignal-1.4.0-py3-none-any.whl (7.5 kB)
Downloading annotated_doc-0.0.5-py3-none-any.whl (5.3 kB)
Downloading anyio-4.15.1-py3-none-any.whl (132 kB)
Downloading attrs-26.1.0-py3-none-any.whl (67 kB)
Downloading certifi-2026.10.23-py3-none-any.whl (135 kB)
Downloading contourpy-1.4.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (383 kB)
Downloading cuda_pathfinder-1.8.4-py3-none-any.whl (62 kB)
Downloading cycler-0.12.1-py3-none-any.whl (8.3 kB)
Downloading filelock-4.2.4-py3-none-any.whl (162 kB)
Downloading fonttools-4.67.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (5.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.4/5.4 MB 54.5 MB/s  0:00:00
Downloading frozenlist-1.8.0-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (242 kB)
Downloading h11-0.16.0-py3-none-any.whl (37 kB)
Downloading httptools-0.9.0-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (552 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 552.8/552.8 kB 59.9 MB/s  0:00:00
Downloading idna-3.20-py3-none-any.whl (69 kB)
Downloading joblib-1.6.0-py3-none-any.whl (306 kB)
Downloading cloudpickle-3.1.2-py3-none-any.whl (22 kB)
Downloading kiwisolver-1.5.1-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (1.5 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.5/1.5 MB 105.5 MB/s  0:00:00
Downloading markupsafe-3.0.4-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (22 kB)
Downloading narwhals-2.27.1-py3-none-any.whl (483 kB)
Downloading networkx-3.7-py3-none-any.whl (2.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 93.2 MB/s  0:00:00
Downloading opentelemetry_api-1.45.1-py3-none-any.whl (60 kB)
Downloading packaging-26.3-py3-none-any.whl (129 kB)
Downloading pillow-13.0.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (7.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.1/7.1 MB 223.9 MB/s  0:00:00
Downloading propcache-0.5.4-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (250 kB)
Downloading pyarrow-26.0.0-cp312-cp312-manylinux_2_28_x86_64.whl (53.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 53.9/53.9 MB 255.7 MB/s  0:00:00
Downloading pydantic-2.14.1-py3-none-any.whl (488 kB)
Downloading pydantic_core-2.50.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.2/2.2 MB 192.7 MB/s  0:00:00
Downloading annotated_types-0.8.0-py3-none-any.whl (13 kB)
Downloading pyparsing-3.3.3-py3-none-any.whl (126 kB)
Downloading python_dateutil-3.0.0-py2.py3-none-any.whl (94 kB)
Downloading python_dotenv-1.2.4-py3-none-any.whl (23 kB)
Downloading pyyaml-6.0.3-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (807 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 807.9/807.9 kB 103.9 MB/s  0:00:00
Downloading regex-2026.9.29-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (807 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 807.8/807.8 kB 100.7 MB/s  0:00:00
Downloading safetensors-0.8.0-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (516 kB)
Downloading scipy-1.18.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (35.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 35.3/35.3 MB 270.7 MB/s  0:00:00
Downloading setuptools-84.2.1-py3-none-any.whl (876 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 876.3/876.3 kB 103.7 MB/s  0:00:00
Downloading six-1.17.0-py2.py3-none-any.whl (11 kB)
Downloading starlette-1.10.0-py3-none-any.whl (80 kB)
Downloading sympy-1.14.0-py3-none-any.whl (6.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.3/6.3 MB 229.6 MB/s  0:00:00
Downloading mpmath-1.3.0-py3-none-any.whl (536 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 536.2/536.2 kB 68.4 MB/s  0:00:00
Downloading threadpoolctl-3.7.0-py3-none-any.whl (26 kB)
Downloading truststore-0.10.5-py3-none-any.whl (19 kB)
Downloading typing_extensions-4.16.0-py3-none-any.whl (45 kB)
Downloading typing_inspection-0.4.4-py3-none-any.whl (14 kB)
Downloading urllib3-2.8.0-py3-none-any.whl (135 kB)
Downloading uvloop-0.23.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (4.5 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.5/4.5 MB 229.7 MB/s  0:00:00
Downloading watchfiles-1.3.0-cp310-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (458 kB)
Downloading websockets-17.3-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (225 kB)
Downloading bleach-6.4.0-py3-none-any.whl (165 kB)
Downloading jupytext-1.19.6-py3-none-any.whl (230 kB)
Downloading markdown_it_py-4.2.0-py3-none-any.whl (91 kB)
Downloading mdurl-0.1.2-py3-none-any.whl (10.0 kB)
Downloading mdit_py_plugins-0.6.1-py3-none-any.whl (66 kB)
Downloading nbformat-5.11.1-py3-none-any.whl (79 kB)
Downloading fastjsonschema-2.22.2-py3-none-any.whl (27 kB)
Downloading jsonschema-4.26.0-py3-none-any.whl (90 kB)
Downloading jsonschema_specifications-2025.9.1-py3-none-any.whl (18 kB)
Downloading jupyter_core-5.9.1-py3-none-any.whl (29 kB)
Downloading platformdirs-4.13.5-py3-none-any.whl (32 kB)
Downloading referencing-0.37.0-py3-none-any.whl (26 kB)
Downloading rpds_py-2026.9.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (371 kB)
Downloading traitlets-5.16.1-py3-none-any.whl (86 kB)
Downloading protobuf-7.36.2-cp310-abi3-manylinux2014_x86_64.whl (343 kB)
Downloading python_slugify-9.1.3-py3-none-any.whl (16 kB)
Downloading text_unidecode-1.3-py2.py3-none-any.whl (78 kB)
Downloading requests-2.34.2-py3-none-any.whl (73 kB)
Downloading charset_normalizer-3.5.2-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (257 kB)
Downloading typer-0.27.3-py3-none-any.whl (123 kB)
Downloading rich-15.0.0-py3-none-any.whl (310 kB)
Downloading pygments-2.21.0-py3-none-any.whl (1.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.3/1.3 MB 190.3 MB/s  0:00:00
Downloading shellingham-1.5.4-py2.py3-none-any.whl (9.8 kB)
Downloading tzdata-2026.5-py2.py3-none-any.whl (347 kB)
Downloading webencodings-0.6.1-py3-none-any.whl (8.7 kB)
Downloading xxhash-4.0.2-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (261 kB)
Installing collected packages: text-unidecode, nvidia-cusparselt-cu13, mpmath, cuda-toolkit, xxhash, websockets, webencodings, uvloop, urllib3, tzdata, typing-extensions, truststore, triton, traitlets, tqdm, threadpoolctl, sympy, six, shellingham, setuptools, safetensors, rpds-py, regex, pyyaml, python-slugify, python-multipart, python-dotenv, pyparsing, pygments, pyarrow, protobuf, propcache, platformdirs, pillow, packaging, nvidia-nvtx, nvidia-nvshmem-cu13, nvidia-nvjitlink, nvidia-nccl-cu13, nvidia-curand, nvidia-cufile, nvidia-cuda-runtime, nvidia-cuda-nvrtc, nvidia-cuda-cupti, numpy, networkx, narwhals, multidict, mdurl, MarkupSafe, kiwisolver, idna, httptools, hf-xet, h11, fsspec, frozenlist, fonttools, filelock, fastjsonschema, dill, cycler, cuda-pathfinder, cloudpickle, click, charset_normalizer, certifi, attrs, annotated-types, annotated-doc, aiohappyeyeballs, yarl, uvicorn, typing-inspection, scipy, requests, referencing, python-dateutil, pydantic-core, opentelemetry-api, nvidia-cusparse, nvidia-cufft, nvidia-cublas, multiprocess, markdown-it-py, jupyter-core, joblib, jinja2, httpcore2, cuda-bindings, contourpy, bleach, anyio, aiosignal, xgboost, watchfiles, starlette, scikit-learn, rich, pydantic, pandas, nvidia-cusolver, nvidia-cudnn-cu13, mdit-py-plugins, matplotlib, kagglesdk, jsonschema-specifications, httpx2, aiohttp, typer, jsonschema, huggingface-hub, fastapi, torch, tokenizers, nbformat, datasets, transformers, jupytext, captum, kaggle

Successfully installed MarkupSafe-3.0.4 aiohappyeyeballs-2.7.1 aiohttp-3.14.5 aiosignal-1.4.0 annotated-doc-0.0.5 annotated-types-0.8.0 anyio-4.15.1 attrs-26.1.0 bleach-6.4.0 captum-0.9.0 certifi-2026.10.23 charset_normalizer-3.5.2 click-8.5.0 cloudpickle-3.1.2 contourpy-1.4.0 cuda-bindings-13.4.4 cuda-pathfinder-1.8.4 cuda-toolkit-13.0.3.0 cycler-0.12.1 datasets-5.1.0 dill-0.4.1 fastapi-0.162.0 fastjsonschema-2.22.2 filelock-4.2.4 fonttools-4.67.0 frozenlist-1.8.0 fsspec-2026.7.0 h11-0.16.0 hf-xet-1.7.0 httpcore2-2.16.0 httptools-0.9.0 httpx2-2.16.0 huggingface-hub-2.3.0 idna-3.20 jinja2-3.1.6 joblib-1.6.0 jsonschema-4.26.0 jsonschema-specifications-2025.9.1 jupyter-core-5.9.1 jupytext-1.19.6 kaggle-2.2.5 kagglesdk-0.1.38 kiwisolver-1.5.1 markdown-it-py-4.2.0 matplotlib-3.11.2 mdit-py-plugins-0.6.1 mdurl-0.1.2 mpmath-1.3.0 multidict-7.2.0 multiprocess-0.70.19 narwhals-2.27.1 nbformat-5.11.1 networkx-3.7 numpy-2.5.4 nvidia-cublas-13.1.1.3 nvidia-cuda-cupti-13.0.85 nvidia-cuda-nvrtc-13.0.88 nvidia-cuda-runtime-13.0.96 nvidia-cudnn-cu13-9.24.0.43 nvidia-cufft-12.0.0.61 nvidia-cufile-1.15.1.6 nvidia-curand-10.4.0.35 nvidia-cusolver-12.0.4.66 nvidia-cusparse-12.6.3.3 nvidia-cusparselt-cu13-0.8.1 nvidia-nccl-cu13-2.30.7 nvidia-nvjitlink-13.4.92 nvidia-nvshmem-cu13-3.4.5 nvidia-nvtx-13.0.85 opentelemetry-api-1.45.1 packaging-26.3 pandas-3.1.0 pillow-13.0.0 platformdirs-4.13.5 propcache-0.5.4 protobuf-7.36.2 pyarrow-26.0.0 pydantic-2.14.1 pydantic-core-2.50.1 pygments-2.21.0 pyparsing-3.3.3 python-dateutil-3.0.0 python-dotenv-1.2.4 python-multipart-0.0.32 python-slugify-9.1.3 pyyaml-6.0.3 referencing-0.37.0 regex-2026.9.29 requests-2.34.2 rich-15.0.0 rpds-py-2026.9.1 safetensors-0.8.0 scikit-learn-1.9.1 scipy-1.18.1 setuptools-84.2.1 shellingham-1.5.4 six-1.17.0 starlette-1.10.0 sympy-1.14.0 text-unidecode-1.3 threadpoolctl-3.7.0 tokenizers-0.23.3 torch-2.14.1 tqdm-4.70.1 traitlets-5.16.1 transformers-5.20.2 triton-3.8.0 truststore-0.10.5 typer-0.27.3 typing-extensions-4.16.0 typing-inspection-0.4.4 tzdata-2026.5 urllib3-2.8.0 uvicorn-0.54.0 uvloop-0.23.0 watchfiles-1.3.0 webencodings-0.6.1 websockets-17.3 xgboost-3.4.1 xxhash-4.0.2 yarl-1.25.1
Installed versions:
python= 3.12.3 (main, Aug 31 2026, 10:18:26) [GCC 13.3.0]
torch= 2.14.1+cu130
transformers= 5.20.2
datasets= 5.1.0
cuda_available= False
TrainingArguments signature= (output_dir: str | None = None, per_device_train_batch_size: int = 8, num_train_epochs: float = 3.0, max_steps: int = -1, learning_rate: float = 5e-05, lr_scheduler_type: transformers.trainer_utils.SchedulerType | str = 'linear', lr_scheduler_kwargs: dict | str | None = None, warmup_steps: float = 0, optim: transformers.training_args.OptimizerNames | str = 'adamw_torch_fused', optim_args: str | None = None, weight_decay: float = 0.0, adam_beta1: float = 0.9, adam_beta2: float = 0.999, adam_epsilon: float = 1e-08, optim_target_modules: None | str | list[str] = None, gradient_accumulation_steps: int = 1, average_tokens_across_devices: bool = True, max_grad_norm: float = 1.0, label_smoothing_factor: float = 0.0, bf16: bool = False, fp16: bool = False, bf16_full_eval: bool = False, fp16_full_eval: bool = False, tf32: bool | None = None, gradient_checkpointing: bool = False, gradient_checkpointing_kwargs: dict[str, typing.Any] | str | None = None, torch_compile: bool = False, torch_compile_backend: str | None = None, torch_compile_mode: str | None = None, use_liger_kernel: bool = False, liger_kernel_config: dict[str, bool] | None = None, use_cache: bool = False, neftune_noise_alpha: float | None = None, torch_empty_cache_steps: int | None = None, auto_find_batch_size: bool = False, logging_strategy: transformers.trainer_utils.IntervalStrategy | str = 'steps', logging_steps: float = 500, logging_first_step: bool = False, log_on_each_node: bool = True, logging_nan_inf_filter: bool = True, include_num_input_tokens_seen: str | bool = 'no', log_level: str = 'passive', log_level_replica: str = 'warning', disable_tqdm: bool | None = None, report_to: None | str | list[str] = 'none', run_name: str | None = None, project: str = 'huggingface', trackio_space_id: str | None = None, trackio_bucket_id: str | None = None, trackio_static_space_id: Union[str, NoneType, Literal[False]] = None, eval_strategy: transformers.trainer_utils.IntervalStrategy | str = 'no', eval_steps: float | None = None, eval_delay: float = 0, per_device_eval_batch_size: int = 8, prediction_loss_only: bool = False, eval_on_start: bool = False, eval_do_concat_batches: bool = True, eval_use_gather_object: bool = False, eval_accumulation_steps: int | None = None, include_for_metrics: list[str] = <factory>, batch_eval_metrics: bool = False, save_only_model: bool = False, save_strategy: transformers.trainer_utils.SaveStrategy | str = 'steps', save_steps: float = 500, save_on_each_node: bool = False, save_total_limit: int | None = None, enable_jit_checkpoint: bool = False, push_to_hub: bool = False, hub_token: str | None = None, hub_private_repo: bool | None = None, hub_model_id: str | None = None, hub_strategy: transformers.trainer_utils.HubStrategy | str = 'every_save', hub_always_push: bool = False, hub_revision: str | None = None, load_best_model_at_end: bool = False, metric_for_best_model: str | None = None, greater_is_better: bool | None = None, ignore_data_skip: bool = False, restore_callback_states_from_checkpoint: bool = False, full_determinism: bool = False, seed: int = 42, data_seed: int | None = None, use_cpu: bool = False, accelerator_config: dict | str | None = None, parallelism_config: typing.Any | None = None, dataloader_drop_last: bool = False, dataloader_num_workers: int = 0, dataloader_pin_memory: bool = True, dataloader_persistent_workers: bool = False, dataloader_prefetch_factor: int | None = None, dataloader_multiprocessing_context: str | None = None, dataloader_in_order: bool = True, remove_unused_columns: bool = True, label_names: list[str] | None = None, train_sampling_strategy: str = 'random', length_column_name: str = 'length', ddp_find_unused_parameters: bool | None = None, ddp_bucket_cap_mb: int | None = None, ddp_broadcast_buffers: bool | None = None, ddp_static_graph: bool | None = None, ddp_backend: str | None = None, ddp_timeout: int = 1800, fsdp: str | None = None, fsdp_config: dict[str, typing.Any] | str | None = None, deepspeed: dict | str | None = None, debug: str | list[transformers.debug_utils.DebugOption] = '', skip_memory_metrics: bool = True, do_train: bool = False, do_eval: bool = False, do_predict: bool = False, resume_from_checkpoint: str | None = None, local_rank: int = -1) -> None
Trainer signature= (model: transformers.modeling_utils.PreTrainedModel | torch.nn.modules.module.Module | None = None, args: transformers.training_args.TrainingArguments | None = None, data_collator: collections.abc.Callable[[list[typing.Any]], dict[str, typing.Any]] | None = None, train_dataset: 'Dataset | IterableDataset | datasets.Dataset | None' = None, eval_dataset: 'Dataset | dict[str, Dataset] | datasets.Dataset | None' = None, processing_class: transformers.tokenization_utils_base.PreTrainedTokenizerBase | transformers.image_processing_utils.BaseImageProcessor | transformers.feature_extraction_utils.FeatureExtractionMixin | transformers.processing_utils.ProcessorMixin | None = None, model_init: collections.abc.Callable[..., transformers.modeling_utils.PreTrainedModel] | None = None, compute_loss_func: collections.abc.Callable | None = None, compute_metrics: collections.abc.Callable[[transformers.trainer_utils.EvalPrediction], dict] | None = None, callbacks: list[transformers.trainer_callback.TrainerCallback] | None = None, optimizers: tuple[torch.optim.optimizer.Optimizer | None, torch.optim.lr_scheduler.LambdaLR | None] = (None, None), optimizer_cls_and_kwargs: tuple[type[torch.optim.optimizer.Optimizer], dict[str, typing.Any]] | None = None, preprocess_logits_for_metrics: collections.abc.Callable[[torch.Tensor, torch.Tensor], torch.Tensor] | None = None)

- Exact installed package versions captured in requirements.txt.
- Environment setup completed: 2026-10-24T20:06:25+00:00
- Kaggle fallback: ~/.kaggle/kaggle.json was not visible in this sandbox despite operator confirmation; no secret contents were accessed.
- Public source selected after verification: https://github.com/microsoft/CodeXGLUE, Devign defect-detection dataset.
- Supporting provenance: https://github.com/testing-cs/vulnerability-detection and https://proceedings.neurips.cc/paper/2019/file/49265d2447bc3bbfe9e76306ce40a31f-Paper.pdf.
- Command: git clone --filter=blob:none --no-checkout https://github.com/microsoft/CodeXGLUE.git /tmp/CodeXGLUE
- Raw Devign files copied unmodified from CodeXGLUE into data/raw/.
- Raw file inventory:
README.md	4209 bytes
code/model.py	1131 bytes
code/run.py	28455 bytes
dataset/preprocess.py	1088 bytes
dataset/test.txt	15318 bytes
dataset/train.txt	122185 bytes
dataset/valid.txt	15295 bytes
evaluator/evaluator.py	1497 bytes
evaluator/predictions.txt	20 bytes
evaluator/test.jsonl	410 bytes
- Dataset acquisition completed: 2026-10-24T20:06:59+00:00

## CHECKPOINT K — dataset acquisition blocked
- Local check found no ~/.kaggle/kaggle.json in this sandbox, despite operator confirmation; no credential contents were accessed.
- The public CodeXGLUE mirror cloned successfully, but its dataset directory contains only train.txt, valid.txt, test.txt index files and preprocess.py; the required function.json with labeled functions is absent.
- Therefore the public mirror cannot produce the required raw Devign dataset, and no data preparation or project code was started.
- Awaiting operator decision: provide/mount Kaggle credentials in this environment, or authorize an alternative public source such as the verified Hugging Face Devign dataset mirror.

## CHECKPOINT K resolution and C. Data preparation
- Operator authorized the public Hugging Face DetectVul/devign mirror as the authoritative fallback.
- Kaggle access was unavailable in this sandbox; the CodeXGLUE mirror was incomplete because function.json was absent.
- Source actually used: https://huggingface.co/datasets/DetectVul/devign
- The raw Hugging Face split exports will be stored unchanged under data/raw/huggingface_devign/.
- Deduplication occurs before fresh splitting; all derived data is written under data/processed/.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Generating train split:   0%|          | 0/21854 [00:00<?, ? examples/s]Generating train split:  41%|████      | 9000/21854 [00:00<00:00, 80396.17 examples/s]Generating train split: 100%|██████████| 21854/21854 [00:00<00:00, 105079.81 examples/s]Generating train split: 100%|██████████| 21854/21854 [00:00<00:00, 101099.56 examples/s]
Generating validation split:   0%|          | 0/2732 [00:00<?, ? examples/s]Generating validation split: 100%|██████████| 2732/2732 [00:00<00:00, 83545.42 examples/s]
Generating test split:   0%|          | 0/2732 [00:00<?, ? examples/s]Generating test split: 100%|██████████| 2732/2732 [00:00<00:00, 99698.43 examples/s]
{
  "dataset": "DetectVul/devign",
  "source_splits": {
    "train": 21854,
    "validation": 2732,
    "test": 2732
  },
  "raw_count_before_deduplication": 27318,
  "deduplicated_count": 25917,
  "near_duplicate_rows_removed": 1401,
  "deduplication_method": "SHA-256 of whitespace-normalized code with comments, strings, and non-keyword identifiers normalized",
  "near_duplicate_threshold": "exact match after identifier normalization (conservative hash-based approximation)",
  "split_method": "stratified random split after deduplication",
  "split_ratios": {
    "train": 0.8,
    "validation": 0.1,
    "test": 0.1
  },
  "seed": 42,
  "split_counts": {
    "train": 20733,
    "validation": 2592,
    "test": 2592
  },
  "split_label_counts": {
    "train": {
      "0": 11204,
      "1": 9529
    },
    "validation": {
      "0": 1400,
      "1": 1192
    },
    "test": {
      "0": 1401,
      "1": 1191
    }
  }
}
{
  "dataset": "DetectVul/devign",
  "raw_rows": 27318,
  "deduplicated_rows": 25917,
  "class_balance_raw": {
    "0": 14858,
    "1": 12460
  },
  "class_balance_deduplicated": {
    "0": 14005,
    "1": 11912
  },
  "code_length_characters": {
    "min": 26,
    "max": 142346,
    "mean": 2023.9647119115602,
    "median": 937.0,
    "p95": 6893.0
  },
  "project_counts": {
    "FFmpeg": 9769,
    "qemu": 17549
  },
  "cwe_type_frequency": {}
}
- Data preparation completed: 2026-10-24T20:11:06+00:00

## D. Baseline model
- Model: word/subword-token TF-IDF (1-2 grams) plus class-balanced Logistic Regression.
- Command: source .venv/bin/activate && python src/baseline.py
/home/ubuntu/vuln-detect-codebert/.venv/lib/python3.12/site-packages/sklearn/linear_model/_logistic.py:1435: FutureWarning: 'n_jobs' has no effect since 1.8 and will be removed in 1.10. You provided 'n_jobs=-1', please leave it unspecified.
  warnings.warn(msg, category=FutureWarning)
{
  "model": "tfidf_logistic_regression",
  "test_size": 2592,
  "accuracy": 0.6099537037037037,
  "precision": 0.5696594427244582,
  "recall": 0.617968094038623,
  "f1": 0.5928312525171164,
  "roc_auc": 0.6610175890916349,
  "confusion_matrix": [
    [
      845,
      556
    ],
    [
      455,
      736
    ]
  ],
  "classification_report": {
    "0": {
      "precision": 0.65,
      "recall": 0.6031406138472519,
      "f1-score": 0.625694187338023,
      "support": 1401.0
    },
    "1": {
      "precision": 0.5696594427244582,
      "recall": 0.617968094038623,
      "f1-score": 0.5928312525171164,
      "support": 1191.0
    },
    "accuracy": 0.6099537037037037,
    "macro avg": {
      "precision": 0.6098297213622291,
      "recall": 0.6105543539429374,
      "f1-score": 0.6092627199275698,
      "support": 2592.0
    },
    "weighted avg": {
      "precision": 0.6130842578259373,
      "recall": 0.6099537037037037,
      "f1-score": 0.61059397307425,
      "support": 2592.0
    }
  },
  "vectorizer": {
    "ngram_range": [
      1,
      2
    ],
    "max_features": 100000,
    "vocabulary_size": 100000
  }
}
- Baseline completed: 2026-10-24T20:11:38+00:00

## E. Fine-tune CodeBERT — GPU CHECKPOINT reached
- Local torch build: 2.14.1+cu130; torch.cuda.is_available(): False; cuda_device_count: 0.
- Wrote src/train_codebert.py using the verified installed signatures: TrainingArguments(eval_strategy=...) and Trainer(processing_class=...).
- Wrote notebooks/train_codebert.ipynb as a self-contained Colab fallback with first-cell imports, recursive zip-layout detection, defensive CUDA/data/install checks, signature inspection, and automatic artifact packaging/download.
- Fine-tuning has not started because this sandbox has no CUDA device.

## J. Full project export verification
- Confirmed data/processed/train.jsonl, validation.jsonl, and test.jsonl contain real rows with code and label fields.
- Export command: zip -r -q /home/ubuntu/vuln-detect-codebert_export.zip vuln-detect-codebert (run from /home/ubuntu; wrapped single top-level folder).
- Archive verification passed: src/train_codebert.py, all three processed JSONL files, splits.json, notebook, and baseline results are present.
- Full export completed: 2026-10-24T20:15:17+00:00
