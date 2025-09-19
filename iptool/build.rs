fn main() {
    if cfg!(target_os = "windows") {
        let mut res = winres::WindowsResource::new();
        res.set_icon("iptool.ico"); // 你的图标文件路径
        res.compile().expect("Failed to compile Windows resources");
    }
}
