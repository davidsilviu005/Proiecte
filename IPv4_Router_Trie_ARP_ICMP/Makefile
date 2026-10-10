CC ?= gcc
CFLAGS ?= -O2 -std=gnu11 -Wall -Wextra
CPPFLAGS += -Iinclude
SOURCES := router.c lib/queue.c lib/list.c lib/lib.c
OBJECTS := $(SOURCES:.c=.o)

.PHONY: all clean
all: router

router: $(OBJECTS)
	$(CC) $(LDFLAGS) -o $@ $(OBJECTS) $(LDLIBS)

%.o: %.c
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

clean:
	rm -f router $(OBJECTS)
