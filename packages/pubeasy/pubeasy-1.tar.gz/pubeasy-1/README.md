# pubeasy

Very rudimental package to create publication-ready figures

Install:

```bash
pip install -q --no-cache --upgrade git+https://github.com/romanodev/pubeasy.git
```


```python
from pubeasy import MakeFigure

case_1 = [2.6336E+01,2.6585E+01,2.4472E+01,2.4955E+01,2.5290E+01]
case_2 = [4.4266E+01,4.2785E+01,4.3035E+01,4.3001E+01,4.2796E+01]
a1 = [473, 764, 1342, 2970, 10485]
a2 = [629, 1090, 1660, 2410, 7232]

f = MakeFigure()
f.add_plot(a1,case_1,name='Sample A',marker=True)
f.add_plot(a2,case_2,name='Sample B',marker=True)
f.add_labels('Number of Elements','Thermal conductivity [Wm$^{-1}$K$^{-1}$]')
f.finalize(grid=True,xscale='log',ylim=[0,60],write = True,show=True)
```
