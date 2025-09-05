package com.example.sentiment_analyzer;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.client.RestTemplate;
import java.util.Collections;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;

@Controller
public class ViewController {

    // 当用户访问网站根目录时，显示我们的主页面
    @GetMapping("/")
    public String index() {
        return "index"; // "index" 对应 "index.html"
    }

    // 当用户提交表单时，处理这个请求
    @PostMapping("/analyze")
    public String analyze(@RequestParam("reviewText") String reviewText, Model model) {

        // 1. 创建一个RestTemplate实例，这是Spring提供的用于调用其他API的工具
        RestTemplate restTemplate = new RestTemplate();

        // 2. 这是我们要调用的Python API的地址
        String pythonApiUrl = "http://127.0.0.1:5000/analyze";

        // 3. 设置请求头，告诉对方我们发送的是JSON
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        // 4. 创建请求体，这是一个简单的Map，会被转换成 {"text": "..."} 的JSON格式
        java.util.Map<String, String> requestBody = Collections.singletonMap("text", reviewText);

        // 5. 将请求头和请求体打包成一个HttpEntity
        HttpEntity<java.util.Map<String, String>> requestEntity = new HttpEntity<>(requestBody, headers);

        // 6. 发送POST请求，并接收返回的结果
        // 我们期望返回一个Map，其中包含 "sentiment" 键
        try {
            @SuppressWarnings("unchecked")
            java.util.Map<String, String> response = restTemplate.postForObject(pythonApiUrl, requestEntity, java.util.Map.class);

            String sentiment = (response != null) ? response.get("sentiment") : "分析失败";
            model.addAttribute("sentimentResult", sentiment);
        } catch (Exception e) {
            // 如果调用失败（比如Python服务没开），显示错误信息
            model.addAttribute("sentimentResult", "错误: 无法连接到分析服务。 " + e.getMessage());
        }

        // 7. 再次返回主页面，这次页面会带上分析结果
        return "index";
    }
}