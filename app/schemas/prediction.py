from pydantic import BaseModel


class CognitiveLoadInput(BaseModel):
    student_id: str
    lesson_id: str
    minute_index: int = 1

    pause_frequency: int
    navigation_count_video: int
    rewatch_segments: int
    playback_rate_change: int
    idle_duration_video: int
    time_on_content: int
    navigation_count_adaptation: int
    revisit_frequency: int
    idle_duration_adaptation: int
    quiz_response_time: int
    error_rate: float
