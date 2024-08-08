c2f:
	code2flow --language=py --no-trimming --output=./flows/$(basename $(FILE)).png $(FILE) 
c2f_function:
	code2flow $(FILES) --language=py --no-trimming --output=./flows/out.png --target-function=$(TARGET_FUNC) --downstream-depth=3
# make c2f_function FILES="concat_audios_refactor.py gpt_and_bert.py" TARGET_FUNC=concatenar_audios
c2f_all:
	make c2f FILE=alerts_tel.py
	make c2f FILE=alerts_wpp.py
	make c2f FILE=concat_audios_refactor.py
	make c2f FILE=gpt_and_bert.py
	make c2f FILE=identity_detections.py
	make c2f FILE=identity_functions.py
	make c2f FILE=tag.py
	make c2f FILE=transcript.py
	make c2f FILE=trim_audios.py
