slint::include_modules!();

fn main() -> Result<(), slint::PlatformError> {
    let ui = JarvisUI::new()?;

    ui.on_mute_pressed(|| {
        println!("Jarvis: Audio protocols silenced.");
    });

    ui.on_access_pc_pressed(|| {
        println!("Jarvis: Opening system mainframe...");
        #[cfg(target_os = "windows")]
        {
            std::process::Command::new("explorer").spawn().unwrap();
        }
    });

    ui.run()
}
