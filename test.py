import ai2thor.controller
import cv2
import numpy as np

print("脚本开始运行")
# 初始化 Controller
controller = ai2thor.controller.Controller(scene="FloorPlan1")

# 初始定位（可以根据需要调整）
controller.step(action="Teleport", position={"x": 0.5, "y": 0.9, "z": -1.0})

# 先初始化拿到所有物体的信息
event = controller.step(action="Initialize")
objects = event.metadata['objects']

# 查找 Knife 和 Shoe
knife = next((obj for obj in objects if obj['objectType'] == 'Knife'), None)
shoe = next((obj for obj in objects if obj['objectType'] == 'Shoe'), None)

if knife and shoe:
    print(f"找到 Knife: {knife['objectId']}")
    print(f"找到 Shoe: {shoe['objectId']}")

    # 移动到 Knife 附近
    controller.step(action="Teleport", position=knife['position'])

    # 拿起 Knife
    controller.step(action="PickupObject", objectId=knife['objectId'])

    # 移动到 Shoe 附近
    controller.step(action="Teleport", position=shoe['position'])

    # 放下 Knife
    controller.step(action="DropHeldObject")

    # 强制调整 Knife 的位置，使它在 Shoe 上面
    new_pos = {
        "x": shoe['position']['x'],
        "y": shoe['position']['y'] + 0.05,  # 稍微高一点避免穿模
        "z": shoe['position']['z']
    }
    controller.step(action="TeleportObject", objectId=knife['objectId'], position=new_pos)

    print("刀已经放到鞋子里，准备截图...")

    # 拿到当前摄像头画面
    frame = controller.last_event.frame  # 这是 RGB 图像，类型是 numpy array (H, W, 3)

    # 保存为图片
    save_path = "knife_in_shoe.png"
    cv2.imwrite(save_path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    print(f"截图已保存到 {save_path}")

else:
    print("未找到 Knife 或 Shoe，请确认场景中有这两种物体！")

controller.stop()
