/** Taken from "The Definitive ANTLR 4 Reference" by Terence Parr */

// Derived from http://json.org
grammar EU4;

eu4format
   : pair+
   ;


color
   : '{' NUMBER NUMBER NUMBER '}'
   ;

obj
   : '{'  pair* '}'
   ;

pair
   : STRING '=' value
   ;

value
   : STRING
   | NUMBER
   |color
   | obj
   ;


STRING
   : [\p{L}_]
   ;



NUMBER
   : '-'? INT ('.' [0-9] +)?
   ;


fragment INT
   : '0' | [1-9] [0-9]*
   ;


// \- since - means "range" inside [...]

WS
   : [ \t\n\r] + -> skip
   ;