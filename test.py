from rgb_matrix import RGB_MATRIX
matrix = RGB_MATRIX()

if __name__ == "__main__":
	while True:
		if not matrix.get_scrolling_state():
			matrix.scroll_text_test(1,"ru","a b c d e")
