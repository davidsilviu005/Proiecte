CXX ?= g++
AR ?= ar
CPPFLAGS += -Ilib/include
CXXFLAGS ?= -O2 -std=c++17 -Wall -Wextra -pthread
LDFLAGS += -pthread
SENDER_LIB := libreliable_udp_sender.a
RECEIVER_LIB := libreliable_udp_receiver.a
COMMON_OBJ := lib/libcommon.o
SENDER_OBJ := lib/libsend.o
RECEIVER_OBJ := lib/librecv.o

.PHONY: all demo clean
all: $(SENDER_LIB) $(RECEIVER_LIB)

$(SENDER_LIB): $(SENDER_OBJ) $(COMMON_OBJ)
	$(AR) rcs $@ $^

$(RECEIVER_LIB): $(RECEIVER_OBJ) $(COMMON_OBJ)
	$(AR) rcs $@ $^

lib/%.o: lib/%.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@

demo: examples/udp_sender examples/udp_receiver

examples/udp_sender: examples/sender.cpp $(SENDER_LIB)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o $@ $< $(SENDER_LIB) $(LDFLAGS)

examples/udp_receiver: examples/receiver.cpp $(RECEIVER_LIB)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o $@ $< $(RECEIVER_LIB) $(LDFLAGS)

clean:
	rm -f $(SENDER_OBJ) $(RECEIVER_OBJ) $(COMMON_OBJ) $(SENDER_LIB) $(RECEIVER_LIB) examples/udp_sender examples/udp_receiver
