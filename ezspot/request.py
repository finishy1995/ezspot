class Request:
    # EZSpot Config
    lau_config_file_path    = None
    lau_config_file         = None
    
    # AWS config
    aws_profile             = None
    aws_region              = None
    aws_access_key_id       = None
    aws_secret_access_key   = None
    
    # Workload config
    wld_fleet_number        = None
    wld_instance_type       = None
    wld_instance_azs        = None
    wld_instance_capacity   = None
    wld_instance_sg         = None
    wld_instance_ami        = None
    wld_instance_key        = None
    wld_instance_subnet     = None
    wld_fleet_tag           = None
    wld_ebs_optimized       = None
    wld_iam_role            = None
    
    # Price config
    prc_product_description = None
    prc_product_timerange   = None
    
    def __init__(self, args):
        for key,value in vars(args).items():
            if hasattr(self, key):
                setattr(self, key, value)
    