LDFLAGS = "-L/usr/local/opt/flex/lib"

TARGET = regexp

all: $(TARGET)

$(TARGET) : regexp.tab.c regexp.yy.c
	$(CC) $(CFLAGS) -o $@ $^ ${LDFLAGS} -lfl

regexp.tab.c regexp.tab.h : regexp.y
	bison -d -v -Wno-conflicts-sr -Wno-conflicts-rr $^

regexp.yy.c : regexp.l
	flex -o $@ $^

clean :
	rm -f $(TARGET) $(TARGET).output $(TARGET).vcg
	rm -f regexp.tab.c regexp.tab.h
	rm -f regexp.yy.c
	rm -f main.1.py

run : $(TARGET)
	cat test.1 | ./$(TARGET)
	python3 main.1.py

