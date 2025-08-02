class ModelTestInterface():
    def test_get_object_list(self):
        raise NotImplementedError("list view not tested")
    
    def test_get_object_detail(self):
        raise NotImplementedError("detail view not tested")

    def test_admin_create_object(self):
        raise NotImplementedError("admin create object not tested")

    def test_normal_user_create_object(self):
        raise NotImplementedError("normal user create object not tested")
    
    def test_unauthenticated_user_create_object(self):
        raise NotImplementedError("unauthenticated user create object not tested")

    def test_admin_update_object(self):
        raise NotImplementedError("admin update object not tested")
    
    def test_normal_user_update_object(self):
        raise NotImplementedError("normal user update object not tested")
    
    def test_unauthenticated_user_update_object(self):
        raise NotImplementedError("unauthenticated user update object not tested")
    
    def test_admin_patch_object(self):
        raise NotImplementedError("admin patch object not tested")
    
    def test_normal_user_patch_object(self):
        raise NotImplementedError("normal user patch object not tested")
    
    def test_unauthenticated_user_patch_object(self):
        raise NotImplementedError("unauthenticated user patch object not tested")
    
    def test_admin_delete_object(self):
        raise NotImplementedError("admin delete object not tested")
    
    def test_normal_user_delete_object(self):
        raise NotImplementedError("normal user delete object not tested")
    
    def test_unauthenticated_user_delete_object(self):
        raise NotImplementedError("unauthenticated user delete object not tested")
    
    