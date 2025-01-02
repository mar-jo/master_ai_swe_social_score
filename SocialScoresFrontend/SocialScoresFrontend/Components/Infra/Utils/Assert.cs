namespace SocialScoresFrontend.Components.Infra.Utils
{
    public static class Assert
    {
        public static void NotNull(object? obj, string message)
        {
            if (obj == null)
            {
                throw new NullReferenceException(message);
            }
        }
    }
}
