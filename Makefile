data:
	cd src/data; \
	python3 make_dataset.py

clean-data-only:
	rm -rf data;

clean:
	rm -rf audio; \
	rm -rf data;