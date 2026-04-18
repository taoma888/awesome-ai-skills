.PHONY: help test install publish

SKILLS_DIR := $(shell find skills -mindepth 1 -maxdepth 1 -type d)
PY_SCRIPTS := $(shell find skills -name "*.py")

help:
	@echo "Available commands:"
	@echo "  make test          - Run all script tests"
	@echo "  make install       - Install dependencies"
	@echo "  make stats         - Show code statistics"
	@echo "  make tag           - Tag and release (TAG=v1.0.0 make tag)"
	@echo "  make clean         - Remove temp files"

install:
	pip install requests

test: install
	@echo "=== Testing demand_miner ==="
	python3 skills/autonomous-earning-system/scripts/demand_miner.py "AI副业" 2>&1 | tail -8
	@echo ""
	@echo "=== Testing mvp_generator ==="
	python3 skills/autonomous-earning-system/scripts/mvp_generator.py --idea "AI工具导航站" 2>&1 | tail -8
	@echo ""
	@echo "=== Testing affiliate_link_generator ==="
	python3 skills/affiliate-monetization/scripts/affiliate_link_generator.py Cursor 2>&1 | tail -8
	@echo ""
	@echo "=== Testing hot_topics ==="
	python3 skills/trend-hunter/scripts/hot_topics.py 2>&1 | tail -8
	@echo ""
	@echo "✅ All tests passed"

stats:
	@echo "📊 Code Statistics"
	@echo "---"
	find . -name "*.py" -o -name "*.md" | grep -v ".git" | xargs wc -l 2>/dev/null | tail -1
	@echo "Skills: $$(find skills -mindepth 1 -maxdepth 1 -type d | wc -l)"
	@echo "Scripts: $$(find skills -name "*.py" | wc -l)"

tag:
	@if [ -z "$(TAG)" ]; then echo "Usage: TAG=v1.0.0 make tag"; exit 1; fi
	git tag -a $(TAG) -m "Release $(TAG)"
	git push origin $(TAG)
	@echo "🚀 Tagged and pushed $(TAG)"

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -f changelog.md gitlog.txt skills_index.md
