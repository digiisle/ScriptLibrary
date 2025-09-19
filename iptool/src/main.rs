use ipnetwork::IpNetwork;
use std::io::{self, Write};
use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};
use std::process;
use std::str::FromStr;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use ctrlc;

fn parse_ip_mask(input: &str) -> Option<IpNetwork> {
    if let Ok(network) = input.parse::<IpNetwork>() {
        return Some(network);
    }

    let parts: Vec<&str> = input.split('/').collect();
    if parts.len() == 2 {
        if let (Ok(ip), Ok(mask)) = (IpAddr::from_str(parts[0]), IpAddr::from_str(parts[1])) {
            IpNetwork::with_netmask(ip, mask).ok()
        } else {
            None
        }
    } else {
        None
    }
}

fn increment_ip(ip: IpAddr) -> Option<IpAddr> {
    match ip {
        IpAddr::V4(ipv4) => Some(IpAddr::V4(Ipv4Addr::from(u32::from(ipv4).checked_add(1)?))),
        IpAddr::V6(ipv6) => Some(IpAddr::V6(Ipv6Addr::from(u128::from(ipv6).checked_add(1)?))),
    }
}

fn decrement_ip(ip: IpAddr) -> Option<IpAddr> {
    match ip {
        IpAddr::V4(ipv4) => Some(IpAddr::V4(Ipv4Addr::from(u32::from(ipv4).checked_sub(1)?))),
        IpAddr::V6(ipv6) => Some(IpAddr::V6(Ipv6Addr::from(u128::from(ipv6).checked_sub(1)?))),
    }
}

fn ip_calculator(ip_net: &str) {
    let separator = "**************************************************";
    match parse_ip_mask(ip_net) {
        Some(network) => {
            let num_addresses: usize = match network.size() {
                ipnetwork::NetworkSize::V4(size) => size as usize,
                ipnetwork::NetworkSize::V6(size) => size as usize,
            };
            let usable_ips = num_addresses.saturating_sub(2);
            let network_ip = network.network();
            let broadcast_ip = network.broadcast();

            let is_private = matches!(network.ip(), IpAddr::V4(ipv4) if ipv4.is_private());

            println!("{}", separator);
            println!("IP版本号： {}", if network.is_ipv4() { 4 } else { 6 });
            println!("是否是私有地址： {}", is_private);
            println!("网络号： {}", network_ip);
            println!("前缀长度： {}", network.prefix());
            println!("子网掩码： {}", network.mask());
            println!("IP地址总数: {}", num_addresses);
            println!("可用IP地址总数： {}", usable_ips);

            if usable_ips > 0 {
                if let (Some(first_usable_ip), Some(last_usable_ip)) =
                    (increment_ip(network_ip), decrement_ip(broadcast_ip))
                {
                    println!("起始可用IP地址： {}", first_usable_ip);
                    println!("最后可用IP地址： {}", last_usable_ip);
                    println!("可用IP地址范围： {} ~ {}", first_usable_ip, last_usable_ip);
                }
            } else {
                println!("没有可用IP地址。");
            }
            println!("广播地址： {}", broadcast_ip);
            println!("{}", separator);
        }
        None => println!("Error: Invalid input format. Use IP/mask or IP/subnet mask."),
    }
}

fn main() {
    let running = Arc::new(AtomicBool::new(true));

    // 监听 Ctrl+C 信号
    let r = running.clone();
    ctrlc::set_handler(move || {
        println!("\nBye! Hope to see you again!");
        r.store(false, Ordering::SeqCst);
        process::exit(0);
    })
    .expect("Error setting Ctrl+C handler");

    println!("欢迎使用本程序！");
    println!("输入 'quit' 退出程序，按 Ctrl+C 强制退出。");

    while running.load(Ordering::SeqCst) {
        print!("请输入IP/mask or IP/subnet：\n");
        io::stdout().flush().unwrap();

        let mut input = String::new();
        if io::stdin().read_line(&mut input).is_err() {
            continue;
        }
        let input = input.trim();

        if input.eq_ignore_ascii_case("quit") {
            println!("\nBye! Hope to see you again!");
            process::exit(0);
        }

        ip_calculator(input);
    }
}
