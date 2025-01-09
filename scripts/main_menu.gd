extends Control




func _on_options_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/options.tscn")
	pass # Replace with function body.


func _on_quit_pressed() -> void:
	get_tree().quit()
	pass # Replace with function body.


func _on_play_main_pressed() -> void:
	get_tree().change_scene_to_file("res://scenes/play_selection.tscn")
	pass # Replace with function body.
