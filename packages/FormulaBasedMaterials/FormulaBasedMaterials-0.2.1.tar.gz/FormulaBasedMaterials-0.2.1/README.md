# FormulaBasedMaterials
Generate Formula-Based Materials into Voxel, STL files

# Usage:

```
pip install FormulaBasedMaterials
```

```python
import matplotlib.pyplot as plt
%matplotlib inline
import FormulaBasedMaterials as FBM

test_SingleFM=FBM.SingleFormulaBasedMaterial(formula='sin(x)*cos(y)+sin(y)*cos(z)+sin(z)*cos(x)+1', l=10, r=[1,1,1], a=[1,1,1], eps=0.2, res=0.2)
test_SingleFM=FBM.SingleFormulaBasedMaterial(unit='random')
test_SingleFM=FBM.SingleFormulaBasedMaterial(unit='SchD')
test_SingleFM=FBM.SingleFormulaBasedMaterial(unit='gyroid')
test_SingleFM.formSolid(save=True,smooth=True)
test_SingleFM.formSurface(save=False)
```
