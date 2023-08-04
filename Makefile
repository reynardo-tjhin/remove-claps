data:
	cd src/data; \
	python3 make_dataset.py

features:
	cd src/features; \
	python3 build_audio_features.py

train:
	cd src/models; \
	python3 train.py

remove_claps:
	cd src; \
	python3 remove_claps.py

clean-data-only:
	rm -rf data;

clean:
	rm -rf audio; \
	rm -rf data;

.PHONY: all data clean