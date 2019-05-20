all:
	cython -3 wrapper.pyx --cplus
	clang++ -stdlib=libc++ -std=c++11 -fPIC -shared -march=native -O2 -fpermissive \
	*.cpp -o module.so \
	`python-config --include` \
	{{ numpy_includes }} \
	{{ python_linalg }} \
	{{ python_lib }}
clean:
	rm -rf *.o
	rm -rf *.so
