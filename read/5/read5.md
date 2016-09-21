#Reading 5, Team C
* [Test case purification for improving fault localization](http://dl.acm.org/citation.cfm?id=2635906)

1. *Reading*
  + Jifeng Xuan and Martin Monperrus. 2014. Test case purification for improving fault localization. Proceedings of the 22nd ACM SIGSOFT International Symposium on Foundations of Software Engineering (FSE 2014).
2. *Keywords*
  1. **Test case purification**: The act of creating a short test case with only one assertion. These are generated through the removal of several statements from a failing test case. The purpose of this is to improve existing techniques on fault localization.
  2. **Assertion**: a binary expression that indicates expected behaviors of a program. An exception is thrown when an assertion is not met. This causes the test case with the assertion to be marked as a failure.
  3. **Test case atomization**: Where a test case with n assertions is turned into n test cases with 1 assertion through test case purification. This generates a set of test cases for each test case that fails.
  4. **Dynamic program slicing**: The act of generating purified test cases by the removal of irrelevant statements. Dynamic slicing keeps the executed statements in a dynamic execution. This reduces the size of test cases needing to be executed.
3. *Notes (4 of 19)*
  1. **Motivational statements**: The paper gives a figure that shows a fraction of a Java program (the Apache Commons Lang lib). The authors took this program and injected a fault at line 20 (negating a conditional expression). After the fault is injected the test cases of AC Lang are run and only one test case fails (t1). The test case covers lines 3 to 21, but when modern fault localization frameworks like Tarantula are run it gives a rank for all lines (3-21) as equal. Because of this result it is hard to know the fault is at line 20.
  2. **Hypotheses**: Since fault localization is an essential and time-consuming activity in software engineering, various fault localization techniques (spectrum-based, mutations, slicing) were created to identify faults in code based on execution traces of test cases. The paper posits that test case purification can improve fault localization performance by separating existing test cases into smaller, "purified", test cases. When combined with the original fault localization techniques, test case purification should result in better ranking of the program statements.
  3. **Related work**: Tarantula is a framework to localize and visualize faults. Ochiai, Jaccard, and Tarantula are seen as the best in spectrum-based fault localization. This paper talks about test case purification as a way to make better use of existing test cases and can be applied to existing techniques like the above. There is also mutation and slicing based fault localization listed in related works. FIFL injects faults (mutants) and ranks edits based on suspiciousness of mutants. Slicing-based fault localization has been used to reduce the size of programs to avoid distributing irrelevant statements or to identify faulty statements. In this work the authors only change test cases for fault localization, not the programs themselves.
  4. **Future work**: Listed for future work is to conduct experiments on other Java projects as a measure of performance for the framework. The authors plan to design new ranking methods and explore how to reduce the time cost of test case slicing for test case purification. Lastly they would like to apply test case purification to other software issues like regression testing and automatic software repair.
4. *Needs improvement*
  1. Some of the results showed that test case purification performed worse than the original techniques running without it because the original techniques reached near optimal ranking, how can people using test case purification detect these test cases to prevent purification causing worsening of performance?
  2. Computation time using test purification rose 4.5x per fault (from about 1 minute to 4.5 minutes) but this was listed as an acceptable time increase (without defining what acceptable or unacceptable is). Is the minimization of wasted effort still better than the time lost per fault when every technique tested was only improved 40% of the time at maximum (and 18% at worse)?
  3. Breadth of test case purification was not addressed. What about non-java projects or non-mutated code (actual faults rather than generated ones)?
5. *Connection to other papers*
  1. **Connection to GZoltar**: This paper implements different fault localization techniques on top of GZoltar. GZoltar is then used to collect the program spectra. The future work of GZoltar listed the minimization of test suites as a future goal, which test case purification solves.