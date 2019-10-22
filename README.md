# seam_carving
content-aware image resizing algorithm

## Usage
```
conda env create --name [new_env_name] --file env.yml
conda activate [new_env_name]
python setup.py build_ext --inplace
python seam_carving.py
```
need to change two points in seam_carving.py before executing
1. change img_path variable to the actual image path
2. change r_rows and r_cols variables to the size you would like to resize
