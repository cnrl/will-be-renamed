all:
	cython -3 wrapper.pyx --cplus
	g++ -std=c++14 -fPIC -shared -march=native -O2 -fpermissive \
	*.cpp -o wrapper.so \
	`python-config --includes` \
	`python-config --ldflags` \
	{{ numpy_includes }}
clean:
	rm -rf *.o
	rm -rf *.so
