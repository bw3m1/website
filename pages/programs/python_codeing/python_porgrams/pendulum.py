import numpy as np
from scipy.integrate import solve_ivp
import pygame

def A(t, y, n, lengths, damping=0):
    theta, omega = y[:n], y[n:]
    dydt = np.zeros_like(y)
    g = 9.81
    for i in range(n):
        dydt[i] = omega[i]
        net_torque = -g / lengths[i] * np.sin(theta[i]) + damping * omega[i]
        for j in range(n):
            if i != j:
                net_torque -= omega[j]**2 * lengths[j] / lengths[i] * np.sin(theta[i] - theta[j])
        dydt[n + i] = net_torque
    return dydt

def B(n, angles, angular_velocities, lengths, damping=0):
    y0 = np.concatenate([angles, angular_velocities])
    t_max = 10
    t_eval = np.linspace(0, t_max, 1000)
    sol = solve_ivp(A, (0, t_max), y0, args=(n, lengths, damping), t_eval=t_eval)
    return sol.t, sol.y

def C(lengths, angles, origin, scale_factor):
    x, y = [origin[0]], [origin[1]]
    for i, length in enumerate(lengths):
        new_x = x[-1] + scale_factor * length * np.sin(angles[i])
        new_y = y[-1] + scale_factor * length * np.cos(angles[i])
        x.append(new_x)
        y.append(new_y)
    return x[1:], y[1:]

def D(screen, n, angles, angular_velocities, lengths, speed_factor, damping, trail_length, selected_item=None, active_item=None, user_input=""):
    font = pygame.font.SysFont("Arial", 30)
    menu_items = [
        f"Number of pendulums: {n}" if selected_item != 0 else f"Number of pendulums: {user_input}",
        f"Angles: {', '.join([f'{angle:.2f}' for angle in angles])}" if selected_item != 1 else f"Angles: {user_input}",
        f"Velocities: {', '.join([f'{v:.2f}' for v in angular_velocities])}" if selected_item != 2 else f"Velocities: {user_input}",
        f"Lengths: {', '.join([f'{length:.2f}' for length in lengths])}" if selected_item != 3 else f"Lengths: {user_input}",
        f"Speed: {speed_factor:.2f}" if selected_item != 4 else f"Speed: {user_input}",
        f"Damping: {damping:.2f}" if selected_item != 5 else f"Damping: {user_input}",
        f"Trail Length: {trail_length}" if selected_item != 6 else f"Trail Length: {user_input}"]
    screen.fill((7, 7, 7))
    for i, item in enumerate(menu_items):
        color = (255, 255, 255) if i != active_item else (255, 200, 0)
        screen.blit(font.render(item, True, color), (50, 100 + i * 40))
    pygame.display.flip()

def show_help(screen):
    font = pygame.font.SysFont("Arial", 30)
    help_text = [
        "Press SPACE to toggle menu.",
        "Press H to toggle this help.",
        "Use UP/DOWN arrows to navigate menu.",
        "Enter values for parameters in menu mode.",
        "Press Q to quit the simulation."]
    screen.fill((7, 7, 7))
    for i, line in enumerate(help_text):
        screen.blit(font.render(line, True, (255, 255, 255)), (50, 100 + i * 40))
    pygame.display.flip()

def E(events, showing_menu, showing_help, paused, selected_item, user_input, n, angles, angular_velocities, lengths, speed_factor, damping, trail_length):
    menu_start_y, item_height = 100, 40
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            return False, showing_menu, showing_help, paused, selected_item, user_input, n, angles, angular_velocities, lengths, speed_factor, damping, trail_length
        elif event.type == pygame.KEYDOWN:
            if showing_menu:
                if event.key == pygame.K_RETURN and selected_item is not None:
                    try:
                        if selected_item == 0:
                            n = max(1, int(user_input))
                            angles = [np.pi / 4] * n
                            angular_velocities = [0.0] * n
                            lengths = [0.4 / n] * n
                        elif selected_item == 1:
                            angles = list(map(float, user_input.split(',')))
                        elif selected_item == 2:
                            angular_velocities = list(map(float, user_input.split(',')))
                        elif selected_item == 3:
                            lengths = list(map(float, user_input.split(',')))
                        elif selected_item == 4:
                            speed_factor = max(0.1, float(user_input))
                        elif selected_item == 5:
                            damping = (max(0, float(user_input)))
                        elif selected_item == 6:
                            trail_length = max(1, int(user_input))
                    except ValueError:
                        print("Invalid input")
                    user_input, selected_item = "", None
                elif event.key == pygame.K_BACKSPACE and selected_item is not None:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_ESCAPE and selected_item is not None:
                    user_input, selected_item = "", None
                elif selected_item is not None:
                    user_input += event.unicode
            if event.key == pygame.K_SPACE:
                if showing_help:
                    showing_help = False
                    showing_menu = True
                else:
                    showing_menu = not showing_menu
                    paused = showing_menu
            elif event.key == pygame.K_h:
                showing_help = not showing_help
                showing_menu = showing_help
                paused = showing_help
            elif event.key == pygame.K_q:
                pygame.quit()
                return False, showing_menu, showing_help, paused, selected_item, user_input, n, angles, angular_velocities, lengths, speed_factor, damping, trail_length
            elif event.key == pygame.K_r:  # R key for randomizing pendulum state
                angles = np.random.uniform(-np.pi / 2, np.pi / 2, size=n)  # Random angles
                angular_velocities = np.random.uniform(-2.0, 2.0, size=n)  # Random velocities
                lengths = np.random.uniform(0.1, 2.0, size=n)  # Random lengths
                print(f"Randomized: angles={angles}, velocities={angular_velocities}, lengths={lengths}")
        elif event.type == pygame.MOUSEBUTTONDOWN and showing_menu:
            x, y_pos = event.pos
            if 50 <= x <= 600:
                for i in range(7):  # Increased to 7 due to new menu items
                    if menu_start_y + i * item_height <= y_pos < menu_start_y + (i + 1) * item_height:
                        selected_item = i
                        user_input = ""
    return True, showing_menu, showing_help, paused, selected_item, user_input, n, angles, angular_velocities, lengths, speed_factor, damping, trail_length

def main():
    pygame.init()
    screen = pygame.display.set_mode((1600, 850))
    clock = pygame.time.Clock()
    n, angles, angular_velocities, lengths = 3, [np.pi / 4, np.pi / 6, np.pi / 8], [0.0, 0.0, 0.0], [0.4 / 3] * 3
    paused, showing_menu, showing_help, k, speed_factor = True, True, False, 0, 1.0
    damping = 0.1  # Default damping factor
    trail_length = 50  # Default trail length
    t, y = B(n, angles, angular_velocities, lengths, damping)
    selected_item, user_input = None, ""
    trail = []

    while True:
        running, showing_menu, showing_help, paused, selected_item, user_input, n, angles, angular_velocities, lengths, speed_factor, damping, trail_length = E(
            pygame.event.get(), showing_menu, showing_help, paused, selected_item, user_input, n, angles, angular_velocities, lengths, speed_factor, damping, trail_length
        )
        if not running:
            break
        screen.fill((7, 7, 7))
        if showing_help:
            show_help(screen)
        elif showing_menu:
            D(screen, n, angles, angular_velocities, lengths, speed_factor, damping, trail_length, selected_item=selected_item, user_input=user_input)
        else:
            if not paused:
                k += speed_factor
                k %= len(t)
                frame_angles = y[:n, int(k)]
                x, y_coords = C(lengths, frame_angles, [screen.get_width() // 2, screen.get_height() // 2], min(screen.get_width(), screen.get_height()) * 0.4 / sum(lengths))
                
                trail.append((x[-1], y_coords[-1]))
                if len(trail) > trail_length:
                    trail.pop(0)
                
                # Draw the trail
                if len(trail) > 1:
                    for i in range(len(trail) - 1):
                        alpha = max(255 - int((i / len(trail)) * 255), 0)
                        color = (0, 255, 0, alpha)
                        pygame.draw.line(screen, color, trail[i], trail[i + 1], 2)
                
                for i in range(n):
                    pygame.draw.line(screen, (0, 255, 255), [screen.get_width() // 2, screen.get_height() // 2] if i == 0 else (x[i - 1], y_coords[i - 1]), (x[i], y_coords[i]), 2)
                    pygame.draw.circle(screen, (0, 255, 255), (int(x[i]), int(y_coords[i])), 4)

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    main()