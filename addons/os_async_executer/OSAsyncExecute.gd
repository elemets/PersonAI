tool
extends Node

onready var thread: Thread = Thread.new()
onready var _mutex: Mutex = Mutex.new()

var _is_running: bool = false

signal command_finished(path, arguments, output, exit_code, identifier)

func _set_is_running(running: bool):
	_mutex.lock()
	_is_running = running
	_mutex.unlock()

func get_is_running() -> bool:
	_mutex.lock()
	var res = _is_running
	_mutex.unlock()
	return res

func execute(path: String, arguments: PoolStringArray, identifier = null):
	while get_is_running():
		yield(Engine.get_main_loop(), "idle_frame")
	_cleanup()
	_execute_shell_command(path, arguments, identifier)

func _execute_shell_command(path: String, arguments: PoolStringArray, identifier):
	_set_is_running(true)
	thread.start(self, "_thread_runner", [path, arguments, identifier])

func _thread_runner(parameters):
	var path: String = parameters[0]
	var args: PoolStringArray = parameters[1]
	var identifier = parameters[2]
	var output: Array = []
	var exit_code := OS.execute(path, args, true, output, true)
	emit_signal("command_finished", path, args, output[0], exit_code, identifier)
	_set_is_running(false)

func _cleanup():
	if thread.is_active() and not get_is_running():
		thread.wait_to_finish()
	
func _exit_tree():
	_cleanup()
