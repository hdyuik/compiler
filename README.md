# a lexer and parser generator

## 简介
  * 一个编译前端的lexer与parser生成器
  * lexer基于递归下降分析正则语言转nfa转dfa进行分词
  * parser使用LALR
  
## 使用
  * lexer部分参考test/lexer_test.py
  * parser部分可以参考test/parser_test.py中的json数字的测试用例

## 部分注意事项
  * 要运行测试, 必须安装graphviz用于输出状态机图以及语法树
  * lexer
    * lexer的正则语法在recognizer完工之后给出
    * lexer正则的支持力度比较小, 仅支持部分正则, 对于超过type 3部分没有支持
  * parser
    * 输入文法的时候请不要使用EOF Terminal, 这部分会自动加入
    * 文法的真实起始符号并不是set_start_symbol时所用的起始符号, 而是一个新的包裹符号, S(wrapper) -> S EOF, 在这里, EOF自动加入
    * 基于文法生成的LALRNFA, 并没有station部分, 因为每一个station只有ε进出, 这部分在构造时被省略

## TODO
  * 补测试
  * 默认dfa的最小化实现
  * re_parser fsm连接
  * 加入debug选项, 输出运行过程数据
    * lexer
      * 递归下降分析正则的过程
      * 生成的nfa
      * nfa转换成的dfa
      * 识别过程
    * parser
      * 文法转换成的lalr_nfa
      * nfa 转换成的 dfa
      * 识别过程中, parsing_stack以及input_stack, 在每一次shift/reduce时的变化