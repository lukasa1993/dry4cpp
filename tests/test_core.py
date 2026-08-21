from dry4cpp.core import find
def test_duplicate(tmp_path):
 a=tmp_path/"a.cpp";b=tmp_path/"b.cpp";s="int f(int x){int y=x+1;if(y>2){y=y*3;}return y;}";a.write_text(s);b.write_text(s.replace("f","g").replace("y","z"));assert find(tmp_path,[a,b],10)
def test_short(tmp_path):
 a=tmp_path/"a.cpp";b=tmp_path/"b.cpp";a.write_text("int f(){return 1;}");b.write_text("int g(){return 2;}");assert find(tmp_path,[a,b],30)==[]
