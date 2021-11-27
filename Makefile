SHELL := /bin/bash

format:
	@find . -name "*.go" | xargs -I {} gofmt -w {}
	@echo "[format] done."

build: format
	@go env -w CGO_ENABLED=0
	@go env -w GOOS=linux
	@go build -o bin/jnuhealth.linux

	@go env -w CGO_ENABLED=0
	@go env -w GOOS=windows
	@go build -o bin/jnuhealth.win

	@go env -w CGO_ENABLED=1
	@go env -w GOOS=darwin
	@go build -o bin/jnuhealth.mac

	@echo "[build] done."

clean:
	@rm -rf bin
	@echo "[clean] done."
