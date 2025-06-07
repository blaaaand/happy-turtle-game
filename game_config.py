class Config:
    # Game Configuration

    # Screen settings
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60

    # Colors
    BG_COLOR = (173, 216, 230)  # Light blue
    TURTLE_COLOR = (0, 150, 0)  # Green
    SHELL_COLOR = (100, 60, 0)  # Brown
    OBSTACLE_COLOR = (255, 0, 0)  # Red
    CORAL_COLOR = (255, 127, 80)  # Coral
    SEAFOAM_COLOR = (175, 238, 238)  # Seafoam green

    # Physics settings
    GRAVITY = 0.5
    JUMP_SPEED = -10
    TURTLE_WIDTH = 50
    TURTLE_HEIGHT = 50
    MAX_FALL_SPEED = 8  # Reduced max fall speed

    # Obstacle settings
    MIN_GAP_SIZE = 200  # Increased minimum gap size
    MAX_GAP_SIZE = 300  # Increased maximum gap size
    
    # Audio settings
    MUSIC_VOLUME = 0.5
    SFX_VOLUME = 0.5
