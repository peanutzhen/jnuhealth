SHELL := /bin/bash

format:
	@find . -name "*.go" | xargs -I {} gofmt -w {}
	@echo "[format] done."

build: format
	@go build -o bin/jnuhealth
	@echo "[build] done."

clean:
	@rm -rf bin
	@echo "[clean] done."
