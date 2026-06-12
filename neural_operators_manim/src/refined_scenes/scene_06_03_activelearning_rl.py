from manim import *
import numpy as np

from src.common.timing import TimedScene
from src.common.theme import *

apply_global_config()

CYAN = "#00FFFF"
GREEN_SCREEN = "#00FF00"

class Scene0603_ActiveLearning_RL(TimedScene):
    SCRIPT_ID = "6.3"
    SCRIPT_TITLE = "Active Learning & RL trong không gian hàm"
    SCRIPT_START = 1600.0
    SCRIPT_END = 1675.0
    SCENE_DURATION = SCRIPT_END - SCRIPT_START

    def construct(self):
        title = Text("Active Learning: Chọn mẫu thông minh", font_size=28,
                     color=OPERATOR, weight=BOLD).to_edge(UP, buff=0.4)
        self.play_timed("b1_title", 0, 2, FadeIn(title))

        cost_title = Text("Chi phí sinh data", font_size=20, color=WARNING).shift(LEFT*4 + UP*1.7)
        
        budget_bar_bg = Rectangle(width=2.5, height=0.4, color=GRAY_B, fill_opacity=0.2, stroke_width=1.5)
        budget_bar_bg.shift(LEFT*4 + UP*0.8)
        budget_bar = Rectangle(width=2.5, height=0.4, color=GREEN_SCREEN, fill_opacity=0.6, stroke_width=0)
        budget_bar.shift(LEFT*4 + UP*0.8)
        budget_label = Text("Budget: $10M", font_size=14, color=GREEN_SCREEN, weight=BOLD).next_to(budget_bar, RIGHT, buff=0.2)
        
        self.play_timed("b1_budget", 2, 5,
                        FadeIn(cost_title),
                        Create(budget_bar_bg),
                        FadeIn(budget_bar),
                        Write(budget_label))

        sim_cost = VGroup(
            Rectangle(width=1.8, height=0.5, color=INPUT, fill_opacity=0.2, stroke_width=1.5),
            Text("Simulation: 2h", font_size=12, color=INPUT)
        ).arrange(DOWN, buff=0.05)
        
        exp_cost = VGroup(
            Rectangle(width=1.8, height=0.5, color=RED, fill_opacity=0.2, stroke_width=1.5),
            Text("Experiment: $500K", font_size=12, color=RED)
        ).arrange(DOWN, buff=0.05)

        VGroup(sim_cost, exp_cost).arrange(RIGHT, buff=0.4).shift(LEFT*4 + DOWN*0.5)

        self.play_timed("b1_costs", 5, 8,
                        FadeIn(sim_cost),
                        FadeIn(exp_cost))

        space_title = Text("Function Space", font_size=20, color=PHYSICS).shift(RIGHT*3 + UP*2.2)
        
        axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 3, 1],
            x_length=4, y_length=2.5,
            axis_config={"color": GRAY_B, "include_ticks": False}
        ).shift(RIGHT*3 + DOWN*0.3)

        np.random.seed(42)
        candidates = VGroup()
        for _ in range(15):
            x = np.random.uniform(0.5, 4.5)
            y = np.random.uniform(0.5, 2.5)
            point = Dot(axes.c2p(x, y), radius=0.06, color=GRAY_B, fill_opacity=0.5)
            candidates.add(point)

        self.play_timed("b1_space", 8, 12,
                        FadeIn(space_title),
                        Create(axes),
                        LaggedStart(*[FadeIn(c, scale=0.5) for c in candidates], lag_ratio=0.1))

        al_title = Text("Active Learning", font_size=18, color=GREEN_SCREEN, weight=BOLD).shift(RIGHT*3 + DOWN*2.2)
        
        selected_indices = [3, 7, 11]
        selected_points = VGroup(*[candidates[i] for i in selected_indices])
        
        uncertainty_glow = VGroup(*[
            Circle(radius=0.2, color=YELLOW, fill_opacity=0.3, stroke_width=0).move_to(p.get_center())
            for p in selected_points
        ])

        self.play_timed("b1_active", 12, 18,
                        FadeIn(al_title),
                        FadeIn(uncertainty_glow),
                        selected_points.animate.set_color(GREEN_SCREEN).set_fill(opacity=1.0),
                        Flash(VGroup(*selected_points), color=GREEN_SCREEN, flash_radius=0.3, line_length=0.15))

        budget_shrink = budget_bar.animate.scale(0.6, about_edge=LEFT)
        budget_update = budget_label.animate.become(
            Text("Budget: $6M", font_size=14, color=YELLOW, weight=BOLD).next_to(budget_bar, RIGHT, buff=0.2)
        )

        self.play_timed("b1_budget_decrease", 18, 21,
                        budget_shrink,
                        budget_update,
                        FadeOut(uncertainty_glow))

        question = Text("Với budget cố định, chọn mẫu ở đâu\nđể giảm uncertainty nhiều nhất?", 
                       font_size=16, color=WARNING, weight=BOLD).to_edge(DOWN, buff=0.5)
        self.play_timed("b1_question", 21, 25, FadeIn(question))

        random_label = Text("Random: Cần 100 samples", font_size=14, color=RED).shift(LEFT*4 + DOWN*1.8)
        active_label = Text("Active: Chỉ cần 20 samples", font_size=14, color=GREEN_SCREEN).shift(RIGHT*3 + DOWN*1.8)

        self.play_timed("b1_comparison", 25, 30,
                        FadeIn(random_label),
                        FadeIn(active_label),
                        Flash(active_label, color=GREEN_SCREEN, flash_radius=0.5))

        self.wait_timed("b1_hold", 30, 35)

        self.play_timed("clear_b1", 35, 37,
                        *[FadeOut(m) for m in [title, cost_title, budget_bar_bg, budget_bar, budget_label,
                                               sim_cost, exp_cost, space_title, axes, candidates,
                                               selected_points, al_title, question, random_label, active_label]])

        rl_title = Text("Reinforcement Learning trong không gian hàm", font_size=26,
                        color=PHYSICS, weight=BOLD).to_edge(UP, buff=0.4)
        self.play_timed("b2_title", 37, 39, FadeIn(rl_title))

        classic_title = Text("Classic RL (Finite-dim)", font_size=18, color=GRAY_B).shift(UP*3.2)
        
        state_box = Rectangle(width=1.6, height=0.9, color=BLUE_C, fill_opacity=0.2, stroke_width=2)
        state_tex = MathTex(r"\mathbf{s} \in \mathbb{R}^n", font_size=24, color=BLUE_C).move_to(state_box)
        state_vec = VGroup(state_box, state_tex).shift(LEFT*4 + UP*2.3)
        
        policy_box = RoundedRectangle(width=1.8, height=1.1, corner_radius=0.15, color=PURPLE, fill_opacity=0.2, stroke_width=2)
        policy_text = VGroup(
            Text("Policy", font_size=21, color=PURPLE, weight=BOLD),
            MathTex(r"\pi", font_size=24, color=PURPLE)
        ).arrange(DOWN, buff=0.05).move_to(policy_box)
        policy = VGroup(policy_box, policy_text).shift(LEFT*1.5 + UP*2.3)
        
        action_box = Rectangle(width=1.6, height=0.9, color=RED, fill_opacity=0.2, stroke_width=2)
        action_tex = MathTex(r"\mathbf{a} \in \mathbb{R}^m", font_size=24, color=RED).move_to(action_box)
        action_vec = VGroup(action_box, action_tex).shift(RIGHT*1 + UP*2.3)
        
        env_box = RoundedRectangle(width=2.5, height=1.1, corner_radius=0.15, color=GREEN_SCREEN, fill_opacity=0.2, stroke_width=2)
        env_tex = Text("Environment", font_size=21, color=GREEN_SCREEN, weight=BOLD).move_to(env_box)
        env = VGroup(env_box, env_tex).shift(RIGHT*3.8 + UP*2.3)
        
        arr1 = Arrow(state_vec.get_right(), policy.get_left(), color=WHITE, buff=0.2, stroke_width=2)
        arr2 = Arrow(policy.get_right(), action_vec.get_left(), color=WHITE, buff=0.2, stroke_width=2)
        arr3 = Arrow(action_vec.get_right(), env.get_left(), color=WHITE, buff=0.2, stroke_width=2)
        arr4 = CurvedArrow(env.get_bottom(), state_vec.get_bottom(), color=WHITE, stroke_width=2, angle=-75 * DEGREES)

        self.play_timed("b2_classic", 39, 45,
                        FadeIn(classic_title),
                        FadeIn(state_vec), FadeIn(policy), FadeIn(action_vec), FadeIn(env),
                        Create(arr1), Create(arr2), Create(arr3), Create(arr4))

        cross = VGroup(
            Line(UR, DL, color=RED, stroke_width=5),
            Line(UL, DR, color=RED, stroke_width=5)
        ).scale(0.3).move_to(arr4.point_from_proportion(0.5))
        strike_label = Text("Không áp dụng cho\nfunction space!", font_size=16, color=RED, weight=BOLD).next_to(cross, UP, buff=0.2)

        self.play_timed("b2_strike", 45, 48,
                        Create(cross),
                        FadeIn(strike_label))

        fs_title = Text("Function-Space RL (Infinite-dim)", font_size=20, color=GREEN_SCREEN, weight=BOLD).shift(DOWN*0.5)
        
        state_func_box = RoundedRectangle(width=2.0, height=1.0, corner_radius=0.15, color=BLUE_C, fill_opacity=0.3, stroke_width=3)
        state_func_tex = MathTex(r"u(x) \in \mathcal{U}", font_size=24, color=BLUE_C).move_to(state_func_box)
        state_func = VGroup(state_func_box, state_func_tex).shift(LEFT*4.2 + DOWN*2.0)
        
        op_policy_box = RoundedRectangle(width=2.4, height=1.3, corner_radius=0.15, color=PURPLE, fill_opacity=0.3, stroke_width=3)
        op_policy_text = VGroup(
            Text("Operator\nPolicy", font_size=21, color=PURPLE, weight=BOLD, line_spacing=0.8),
            MathTex(r"\Pi", font_size=24, color=PURPLE)
        ).arrange(DOWN, buff=0.05).move_to(op_policy_box)
        op_policy = VGroup(op_policy_box, op_policy_text).shift(LEFT*1.2 + DOWN*2.0)
        
        action_func_box = RoundedRectangle(width=2.0, height=1.0, corner_radius=0.15, color=RED, fill_opacity=0.3, stroke_width=3)
        action_func_tex = MathTex(r"a(x) \in \mathcal{A}", font_size=24, color=RED).move_to(action_func_box)
        action_func = VGroup(action_func_box, action_func_tex).shift(RIGHT*1.6 + DOWN*2.0)
        
        func_env_box = RoundedRectangle(width=2.6, height=1.3, corner_radius=0.15, color=GREEN_SCREEN, fill_opacity=0.3, stroke_width=3)
        func_env_tex = Text("PDE\nEnvironment", font_size=21, color=GREEN_SCREEN, weight=BOLD).move_to(func_env_box)
        func_env = VGroup(func_env_box, func_env_tex).shift(RIGHT*4.5 + DOWN*2.0)
        
        farr1 = Arrow(state_func.get_right(), op_policy.get_left(), color=GREEN_SCREEN, buff=0.2, stroke_width=3)
        farr2 = Arrow(op_policy.get_right(), action_func.get_left(), color=GREEN_SCREEN, buff=0.2, stroke_width=3)
        farr3 = Arrow(action_func.get_right(), func_env.get_left(), color=GREEN_SCREEN, buff=0.2, stroke_width=3)
        farr4 = CurvedArrow(func_env.get_bottom(), state_func.get_bottom(), color=GREEN_SCREEN, stroke_width=3, angle=-75 * DEGREES)

        self.play_timed("b2_func_rl", 48, 55,
                        FadeIn(fs_title),
                        FadeIn(state_func), FadeIn(op_policy), FadeIn(action_func), FadeIn(func_env),
                        Create(farr1), Create(farr2), Create(farr3), Create(farr4))

        glow_rect = SurroundingRectangle(VGroup(state_func, op_policy, action_func, func_env), 
                                         color=GREEN_SCREEN, buff=0.3, stroke_width=2)
        
        self.play_timed("b2_glow", 55, 58,
                        Create(glow_rect),
                        Flash(glow_rect, color=GREEN_SCREEN, flash_radius=2.0, line_length=0.3))

        apps = VGroup(
            Text("• Điều khiển dòng chảy", font_size=16, color=WHITE),
            Text("• Can thiệp khí hậu", font_size=16, color=WHITE),
            Text("• Tối ưu thiết kế", font_size=16, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).shift(DOWN*3.5)

        self.play_timed("b2_apps", 58, 62,
                        LaggedStart(*[FadeIn(app, shift=RIGHT*0.2) for app in apps], lag_ratio=0.2))

        self.wait_timed("b2_hold", 62, 73)

        self.play_timed("cut", 73, 75, *[FadeOut(m, run_time=0.4) for m in self.mobjects])
        self.pad_to(self.SCENE_DURATION)
