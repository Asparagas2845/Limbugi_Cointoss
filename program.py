import tkinter as tk
from tkinter import messagebox
from math import comb

class Skill:
    def __init__(self, base_power, coin_power, coin_count, sanity, level):
        self.base = base_power
        self.coin = coin_power
        self.count = coin_count
        self.sanity = sanity
        self.level = level

    def outcome_probabilities(self):
        prob_heads = (50 + self.sanity) / 100
        dist = {}
        for k in range(self.count + 1):
            p = comb(self.count, k) * (prob_heads ** k) * ((1 - prob_heads) ** (self.count - k))
            total_power = self.base + self.coin * k
            dist[total_power] = dist.get(total_power, 0) + p
        return dist


def win_probability(skill_a, skill_b):
    a_dist = skill_a.outcome_probabilities()
    b_dist = skill_b.outcome_probabilities()
    win_prob = draw_prob = 0.0
    level_diff = skill_a.level - skill_b.level
    a_buff = max(level_diff // 3, 0)
    b_buff = max((-level_diff) // 3, 0)
    for a_power, a_p in a_dist.items():
        for b_power, b_p in b_dist.items():
            a_final = a_power + a_buff
            b_final = b_power + b_buff
            if a_final > b_final:
                win_prob += a_p * b_p
            elif a_final == b_final:
                draw_prob += a_p * b_p
    lose_prob = 1.0 - win_prob - draw_prob
    return win_prob, lose_prob, draw_prob


def run_simulation():
    try:
        my = Skill(
            int(my_base.get()), int(my_coin.get()), int(my_count.get()),
            int(my_sanity.get()), int(my_level.get())
        )
        enemy = Skill(
            int(enemy_base.get()), int(enemy_coin.get()), int(enemy_count.get()),
            int(enemy_sanity.get()), int(enemy_level.get())
        )
        # sanity validation
        san_min, san_max = (-50, 50) if allow_ext.get() else (-45, 45)
        if not (san_min <= my.sanity <= san_max):
            raise ValueError(f"자신의 정신력은 {san_min}~{san_max} 사이여야 합니다.")
        if not (san_min <= enemy.sanity <= san_max):
            raise ValueError(f"상대의 정신력은 {san_min}~{san_max} 사이여야 합니다.")

        win, lose, draw = win_probability(my, enemy)
        total = win + lose
        # no decided results
        if total == 0:
            messagebox.showwarning("경고", "무승부 외의 결과가 없어 승패 비율을 계산할 수 없습니다.")
            return
        norm_win = win / total
        norm_lose = lose / total
        win_var.set(f"{norm_win*100:.2f}%")
        lose_var.set(f"{norm_lose*100:.2f}%")
    except ValueError as e:
        messagebox.showerror("입력 오류", str(e))

# main window
root = tk.Tk()
root.title("림버스 컴퍼니 – 합 승률 계산기")
root.geometry("900x600")
root.resizable(False, False)

label_font = ("TkDefaultFont", 24)
entry_font = ("TkDefaultFont", 24)
button_font = ("TkDefaultFont", 18)

# left and right frames
frame_width, frame_height = 420, 320
left_frame = tk.LabelFrame(root, text="자신의 스킬", font=label_font, padx=10, pady=10)
left_frame.place(x=20, y=20, width=frame_width, height=frame_height)
right_frame = tk.LabelFrame(root, text="상대의 스킬", font=label_font, padx=10, pady=10)
right_frame.place(x=460, y=20, width=frame_width, height=frame_height)

# configure grid inside frames to center contents
def setup_frame(frame, var_list):
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    labels = ["기본 위력:", "코인 위력:", "코인 개수:", "공격 레벨:", "정신력:"]
    for i, (text, var) in enumerate(zip(labels, var_list)):
        lbl = tk.Label(frame, text=text, font=label_font)
        ent = tk.Entry(frame, textvariable=var, font=entry_font, width=6, justify='center')
        lbl.grid(row=i, column=0, pady=8, sticky='e')
        ent.grid(row=i, column=1, pady=8, sticky='w')

# variables
my_vars = [tk.StringVar() for _ in range(5)]
enemy_vars = [tk.StringVar() for _ in range(5)]
my_base, my_coin, my_count, my_level, my_sanity = my_vars
enemy_base, enemy_coin, enemy_count, enemy_level, enemy_sanity = enemy_vars

setup_frame(left_frame, my_vars)
setup_frame(right_frame, enemy_vars)

# option checkbox
allow_ext = tk.BooleanVar()
chk = tk.Checkbutton(root, text="정신력 제한 해제\n(-50 ~ 50)", variable=allow_ext, font=label_font)
chk.place(x=20, y=360)

# clash button
btn = tk.Button(root, text="CLASH!", command=run_simulation, font=button_font, width=8, height=2)
btn.place(x=390, y=390)

# result frame centered under CLASH button
win_var = tk.StringVar(value="000.00%")
lose_var = tk.StringVar(value="000.00%")
result_frame = tk.Frame(root)
# place frame at center x of window, y=540
result_frame.place(relx=0.5, y=480, anchor='n')
tk.Label(result_frame, text="승리 확률: ", font=label_font).pack(side='left')
tk.Label(result_frame, textvariable=win_var, font=label_font).pack(side='left')
tk.Label(result_frame, text="   |   ", font=label_font).pack(side='left')
tk.Label(result_frame, text="패배 확률: ", font=label_font).pack(side='left')
tk.Label(result_frame, textvariable=lose_var, font=label_font).pack(side='left')

root.mainloop()
