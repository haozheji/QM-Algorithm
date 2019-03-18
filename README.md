# QM-Algorithm
Python implementation of QM-algorithm

## Introduction
QM algorithm (short for Quine–McCluskey algorith is a method used to minimize Boolean functions. For more details, see this [wiki link](https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm).

## Usage
This program takes minterms as inputs. e.g.

$$
f(A,B,C,D)=\sum m(4,8,10,11,12,15)+d(9,14)
$$ 

To understand this Boolean function more comprehensively, we write it as a table.

| |A|B|C|D|**f**|
|$m_0$|0|0|0|0|0|
|$m_1$|0|0|0|1|0|
|$m_2$|0|0|1|0|0|
|$m_3$|0|0|1|1|0|
|$m_4$|0|1|0|0|1|
|...|...|...|...|...|...|
|$m_14$|1|1|1|0|x|
|$m_15|1|1|1|1|1|

where `x` in the table means we don't care the output.

Then, create `test_case.txt` and prepare the inputs as follows:
```python
4
6
4 8 10 11 12 15
2
9 14
```
The first row indicates **the number of variables**, here we have `A, B, C, D`.

The second row indicates **the number of minterms**.

The third row lists **the minterms**.

The fourth row indicates **the number of don't-care terms**.

The fifth row lists **the don't-care terms**.

