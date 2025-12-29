.PHONY: demo install test clean

# Install all dependencies
install:
	cd bridge/ts-producer && npm install
	cd bridge/py-consumer && pip install -r requirements.txt

# Run the demo: produce bundles and consume them
demo: clean
	@echo "🚀 Running hybrid connectivity bridge demo..."
	@mkdir -p staging output
	@echo "📦 Producing bundles..."
	cd bridge/ts-producer && npm run produce
	@echo "✅ Bundles created in staging/"
	@echo ""
	@echo "🔍 Consuming bundles..."
	cd bridge/py-consumer && python -m src.consumer
	@echo "✅ Processing complete. Check output/"

# Run tests
test:
	cd bridge/ts-producer && npm test
	cd bridge/py-consumer && pytest

# Clean staging and output
clean:
	rm -rf staging output
	mkdir -p staging output
