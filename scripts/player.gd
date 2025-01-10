class_name Player
extends CharacterBody2D


const SPEED = 300.0
const JUMP_VELOCITY = -400.0

const scene: PackedScene = preload("res://scenes/player.tscn")

static func new_player() -> Player:
	var new_player: Player = scene.instantiate()
	return new_player

func update_position(new_position: Vector2):
	position = new_position
