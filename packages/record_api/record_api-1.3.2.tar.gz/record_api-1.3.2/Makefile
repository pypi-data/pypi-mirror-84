.PHONY: groupby_location clean_groupby_location clean_api clean_raw clean_typing clean all test


# .INTERMEDIATE: $(addprefix data/groupby_location/,$(addsuffix .jsonl,$(LIBRARIES)))

all: data/typing/numpy.py

test:
	env PYTEST_DISABLE_PLUGIN_AUTOLOAD=true \
		pytest record_api/test.py


clean: clean_groupby_location clean_api clean_typing clean_raw

clean_typing:
	rm -f data/typing/*


data/typing/numpy.py: data/api.json
	env PYTHON_RECORD_API_OUTPUT=data/typing \
		PYTHON_RECORD_API_INPUT="$^"\
		python -m record_api.write_api

clean_api:
	rm -f data/api.json data/api/*


data/api.json: $(wildcard data/api/*)
	env PYTHON_RECORD_API_OUTPUT=$@ \
		PYTHON_RECORD_API_INPUTS="$^"\
		python -m record_api.combine_apis


data/api/%.json: data/groupby_location/%.jsonl
	env PYTHON_RECORD_API_OUTPUT=$@ \
		PYTHON_RECORD_API_INPUT=$< \
		PYTHON_RECORD_API_LABEL=$(*F) \
		PYTHON_RECORD_API_MODULES=pandas,numpy \
		python -m record_api.infer_apis


clean_groupby_location:
	rm -f data/groupby_location/*


data/groupby_location/%.jsonl: | data/raw/%.jsonl
	env PYTHON_RECORD_API_OUTPUT=$@ \
		PYTHON_RECORD_API_INPUT=$| \
		python -m record_api.line_counts


clean_raw:
	rm -f data/raw/*

data/raw/sample-usage.jsonl:
	env PYTHON_RECORD_API_OUTPUT_FILE=$@ \
		PYTHON_RECORD_API_TO_MODULES=numpy \
		PYTHON_RECORD_API_FROM_MODULES=record_api.sample_usage \
		python -m record_api

