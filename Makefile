LDFLAGS = "-L/usr/local/opt/flex/lib"

TARGET = regexfinal

all: $(TARGET)

$(TARGET) : regexp.tab.c regexp.yy.c
	$(CC) $(CFLAGS) -o $@ $^ ${LDFLAGS} -ly -lfl

regexp.tab.c regexp.tab.h : regexp.y
	bison -d -v $^

regexp.yy.c : regexp.l
	flex -o $@ $^

clean :
	rm -f $(TARGET) $(TARGET).output $(TARGET).vcg
	rm -f regexp.tab.c regexp.tab.h
	rm -f regexp.yy.c

run : $(TARGET)
	cat test.1 | ./$(TARGET)
	python3.14 main.1.py

