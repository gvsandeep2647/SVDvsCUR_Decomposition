<h1>SVD vs CUR Decomposition</h1>

<b>Course Number :</b> CS F469

<b>Contributors : </b>
<ul>
<li>G V Sandeep</li>
<li>Kushagra Agrawal</li>
<li>Snehal Wadhwani</li>
</ul>

<h3><b>Aim :</b> To compare the SVD vs CUR Decomposition on given set of recommendations</h3>

<b>Language :</b> Python v2.7.12
<h6>Working :</h6>
<ol>
<li>The input from the corpus is handled and a matrix of user-movie ratings is made in all the files.</li>
<li>The file 'single_iter_svd_.py' decomposes the ratings matrix into the appropriate U, sigma and V matrices based on the eigenvalues and eigenvectors calculated using python's numpy package.</li>
<li>The file 'multi_iter_svd.py' chooses the best rank-k approximation of the svd among the possible orthonormal matrices for U and V. </li>
<li>The file 'cur.py' performs the CUR decompsition on the ratings matrix in a manner similar to the previous two files that give the SVD decomposition.</li>
</ol>

<h6>Setting up:</h6>
<ol>
<li> Install python's numpy package. </li>
<li> Run single_iter_svd.py, multi_iter_svd.py and cur.py for the comparison between the two decompositions.
</ol>
