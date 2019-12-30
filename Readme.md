# Python scripts for preprocessing airfoils used in [Webfoil](http://webfoil.engin.umich.edu/)

## Usage

### Approach 1 (Recommended)

The `all_in_one/picked_uiuc` folder contains 1433 selected UIUC airfoils in a uniform format (201 coordinates).
If you want to use more coordinates, just modify the 35th line in `all_in_one/step3.py` file, and then run:
`python step3.py`


### Approach 2

This folder contains three python scripts to preprocess airfoils.
You could download the airfoil data from [UIUC airfoil database](http://m-selig.ae.illinois.edu/ads/coord_database.html) and [Webfoil](http://mdolab.engin.umich.edu/webfoil). Then run the scripts in the `original` folder one by one:

- Step 1: Format Data. Remove unnesessary texts from the files and eliminate incomplete airfoils.
- Step 2: Uniform Data. Sharpen airfoils' trailing edges and uniform them.
- Step 3: Select Data. Remove non-smooth airfoils.

After these treatments, you will obtain airfoils of the same format.


## Licensing
Distributed using the GNU Lesser General Public License (LGPL); see the LICENSE file for details.

Just a polite request, please cite the author's papers listed below for which you find it useful.

- Data-based approach for fast airfoil analysis and optimization, _AIAA Journal_ (2019), DOI: [10.2514/1.J057129](https://doi.org/10.2514/1.J057129)
- Data-driven constraint approach to ensure low-speed performance in transonic aerodynamic shape optimization, _Aerospace Science and Technology_ (2019) DOI: [10.1016/j.ast.2019.06.008](https://doi.org/10.1016/j.ast.2019.06.008)

## Contact and Feedback
If you have questions, comments, problems, or want to report a bug, please contact the author:

Jichao Li (cfdljc@gmail.com)




