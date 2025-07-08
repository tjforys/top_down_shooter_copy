class Movement:
    @staticmethod
    def put_back_in_arena_if_outside(area_x, area_y, obj_x, obj_y):
        if obj_x < 0:
            obj_x = 0
        if obj_x > area_x:
            obj_x = area_x
        if obj_y < 0:
            obj_y = 0
        if obj_y > area_y:
            obj_y = area_y

        return obj_x, obj_y


    @staticmethod
    def is_inside_arena(area_x, area_y, obj_x, obj_y) -> bool:
        if area_x > obj_x > 0 and area_y > obj_y > 0:
            return True
        return False
