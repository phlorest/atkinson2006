all: summary.trees

summary.trees: raw/MayanSwd100_3_12_05bn30chrono.t
	cp $< cldf/$@
