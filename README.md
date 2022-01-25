# JointEmbedding
Master thesis project

ARQMath 2020 Challenge focuses mainly on retrieving answers to mathematical questions (Task 1), and formula retrieval (Task 2). 
This project is mainly focused on solving Task 2 of ARQMath Challenge, where a novel method is proposed for formula retrieval.
The method takes formulas in LATEX format, their context words and uses the method of joint
embedding to combine their vector spaces. With the help of a similarity score, a ranked list of
formulas is obtained which is compared against the user’s query formula. The proposal has two
variants: (i) using the entire formulas for training and (ii) splitting the formulas as LATEX tokens
for training. The evaluation metrics used were nDCG’, mAP, p@10. The results were compared
against the gold dataset (qrel file) which is obtained from human assessment methods of pooling
and annotation. The proposed method gave promising results by extracting the relevant formulas
either as an exact match or as a subexpression match as that of the query formula. But overall,
it performed poorly when compared to the baseline method, Tangent-S. Improvement in terms
of searching and ranking methodology could be done for better results. This novel approach
opens the door of opportunities to explore more in the area of formula embedding using machine
translation models.
