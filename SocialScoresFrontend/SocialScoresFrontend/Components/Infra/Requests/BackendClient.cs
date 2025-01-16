using SocialScoresFrontend.Components.Models;
using System.Text;
using System.Text.Json;

namespace SocialScoresFrontend.Components.Infra.Requests
{
    public class BackendClient
    {
        public string BaseUrl { get; init; }

        public BackendClient(HttpClient client, string baseUrl)
        {
            _client = client;
            BaseUrl = baseUrl;
        }

        public async Task<T> Get<T>(string route)
        {
            try
            {
                var response = await _client.GetAsync($"{BaseUrl}{route}");
                response.EnsureSuccessStatusCode();
                string json = await response.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<T>(json) ?? throw new NullReferenceException();
            }
            catch (Exception ex)
            {
                // ToDo: log exception
                throw;
            }
        }

        public async Task GetCustom(string route, Action<HttpResponseMessage> action)
        {
            try
            {
                var response = await _client.GetAsync($"{BaseUrl}{route}");
                response.EnsureSuccessStatusCode();
                action(response);
            }
            catch (Exception ex)
            {
                throw;
            }
        }

        public async Task<T> Post<T>(string route, object payload)
        {
            try
            {
                var jsonPayload = JsonSerializer.Serialize(payload);
                var content = new StringContent(jsonPayload, Encoding.UTF8, "application/json");

                var response = await _client.PostAsync($"{BaseUrl}{route}", content);
                response.EnsureSuccessStatusCode();

                string json = await response.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<T>(json) ?? throw new NullReferenceException();
            }
            catch (Exception ex)
            {
                // ToDo: log exception
                throw;
            }
        }

        public async Task<T> PostForm<T>(string route, params FormDataItem[] formDataItems)
        {
            try
            {
                using var formData = new MultipartFormDataContent();
                foreach (FormDataItem item in formDataItems)
                {
                    if (item.Value is string stringValue)
                    {
                        // Add string content
                        formData.Add(new StringContent(stringValue), item.Name);
                    }
                    else if (item.Value is FileData file)
                    {
                        // Add file content (file details are passed)
                        var fileContent = new ByteArrayContent(file.Data);
                        if(string.IsNullOrEmpty(file.MimeType) == false)
                            fileContent.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue(file.MimeType);
                        if (string.IsNullOrEmpty(file.FileName))
                            file.FileName = "unknown.png";
                        formData.Add(fileContent, item.Name, file.FileName);
                    }
                    else
                    {
                        throw new ArgumentException($"Unsupported data type for item {item.Name}");
                    }
                }

                HttpResponseMessage response = await _client.PostAsync($"{BaseUrl}{route}", formData);
                response.EnsureSuccessStatusCode();

                string json = await response.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<T>(json) ?? throw new NullReferenceException();
            }
            catch (Exception ex)
            {
                // ToDo: log exception
                throw;
            }
        }

        private readonly HttpClient _client;
    }
}
