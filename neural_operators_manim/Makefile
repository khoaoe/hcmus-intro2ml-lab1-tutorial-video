VENV ?= .venv
LOCAL_MANIM := $(VENV)/bin/manim
MANIM ?= $(if $(wildcard $(LOCAL_MANIM)),$(LOCAL_MANIM),manim)
QUALITY ?= h
FILE ?=
SCENE ?=

.PHONY: help check-manim preview render \
	s01_1 s01_2 s01_3 s01_4 s01_5 \
	s02_1 s02_2 s02_3 s02_4 \
	s03 s04 s05 s06 s07 s08

help:
	@echo "Usage:"
	@echo "  make preview FILE=src/.../scenes.py SCENE=ClassName [QUALITY=l|m|h|p|k]"
	@echo "  make render  FILE=src/.../scenes.py SCENE=ClassName [QUALITY=l|m|h|p|k]"
	@echo ""
	@echo "Scene shortcuts:"
	@echo "  s01_1 s01_2 s01_3 s01_4 s01_5"
	@echo "  s02_1 s02_2 s02_3 s02_4"
	@echo "  s03 s04 s05 s06 s07 s08"

check-manim:
	@if ! command -v "$(MANIM)" >/dev/null 2>&1; then \
		echo "Manim executable not found: $(MANIM)"; \
		echo "Activate your environment first (example):"; \
		echo "  micromamba activate manim_env"; \
		echo "Or run directly:"; \
		echo "  micromamba run -n manim_env make s01_1"; \
		echo "If needed, install packages:"; \
		echo "  pip install manim numpy scipy jupyterlab"; \
		exit 127; \
	fi

preview: check-manim
	@test -n "$(FILE)" || (echo "Missing FILE. Example: FILE=src/s01_traditional_dl/scenes.py" && exit 1)
	@test -n "$(SCENE)" || (echo "Missing SCENE. Example: SCENE=Scene1_1_Hook" && exit 1)
	$(MANIM) -p -q$(QUALITY) $(FILE) $(SCENE)

render: check-manim
	@test -n "$(FILE)" || (echo "Missing FILE. Example: FILE=src/s01_traditional_dl/scenes.py" && exit 1)
	@test -n "$(SCENE)" || (echo "Missing SCENE. Example: SCENE=Scene1_1_Hook" && exit 1)
	$(MANIM) -q$(QUALITY) $(FILE) $(SCENE)

s01_1:
	$(MAKE) preview FILE=src/s01_traditional_dl/scenes.py SCENE=Scene1_1_Hook

s01_2:
	$(MAKE) preview FILE=src/s01_traditional_dl/scenes.py SCENE=Scene1_2_PlotTwist

s01_3:
	$(MAKE) preview FILE=src/s01_traditional_dl/scenes.py SCENE=Scene1_3_GridMismatch

s01_4:
	$(MAKE) preview FILE=src/s01_traditional_dl/scenes.py SCENE=Scene1_4_TraditionalSolvers

s01_5:
	$(MAKE) preview FILE=src/s01_traditional_dl/scenes.py SCENE=Scene1_5_Teaser

s02_1:
	$(MAKE) preview FILE=src/s02_ml_function_spaces/scenes.py SCENE=Scene2_1_ScientificData

s02_2:
	$(MAKE) preview FILE=src/s02_ml_function_spaces/scenes.py SCENE=Scene2_2_NotAnImage

s02_3:
	$(MAKE) preview FILE=src/s02_ml_function_spaces/scenes.py SCENE=Scene2_3_ShiftToOperators

s02_4:
	$(MAKE) preview FILE=src/s02_ml_function_spaces/scenes.py SCENE=Scene2_4_ChallengesAndDefinition

s03:
	$(MAKE) preview FILE=src/s03_prerequisites/scenes.py SCENE=PlaceholderScene

s04:
	$(MAKE) preview FILE=src/s04_nn_to_no/scenes.py SCENE=PlaceholderScene

s05:
	$(MAKE) preview FILE=src/s05_scientific_comp/scenes.py SCENE=PlaceholderScene

s06:
	$(MAKE) preview FILE=src/s06_uncertainty_quant/scenes.py SCENE=PlaceholderScene

s07:
	$(MAKE) preview FILE=src/s07_generative_models/scenes.py SCENE=PlaceholderScene

s08:
	$(MAKE) preview FILE=src/s08_open_problems/scenes.py SCENE=PlaceholderScene