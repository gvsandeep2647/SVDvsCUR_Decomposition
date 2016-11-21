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
<li>A function defined in <code>common.py</code> handles the input from the corpus and a matrix of user-movie ratings is made. This function is used by all other files that use the user-movie ratings matrix.</li>
<li>The file <code>single_iter_svd_.py</code> (which uses functions defined in <code>svd.py</code>) decomposes the ratings matrix into the appropriate U, sigma and V matrices based on the eigenvalues and eigenvectors calculated using python's numpy package.</li>
<li>The file <code>multi_iter_svd.py</code>(which uses functions defined in <code>svd.py</code>) chooses the best rank-k approximation of the svd among the possible orthonormal matrices for U and V. </li>
<li>The file <code>cur_replace.py</code> performs the CUR decomposition on the ratings matrix in a manner similar to the previous two files that give the SVD decomposition.</li>This file uses the svd function defined in <code>svd.py</code> for one of its intermediate steps.
</ol>

<h6>Setting up:</h6>
<ol>
<li> Install python's <code>numpy</code> package. </li>
<li> Run <code>single_iter_svd.py, multi_iter_svd.py</code> and <code>cur.py</code> for the comparison between the two decompositions.
</ol>
