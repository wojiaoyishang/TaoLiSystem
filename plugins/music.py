# {"Name": "音乐测试","Version": "v0.0.1","Master": "官方示例","Description": "用于测试", "More": "由以赏修改"}
import audio
import gc;gc.collect()
import machine


audio.player_init(i2c)
audio.set_volume(100)
audio.play('a.mp3')