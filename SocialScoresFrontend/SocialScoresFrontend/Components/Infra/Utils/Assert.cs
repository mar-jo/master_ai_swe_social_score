
namespace SocialScoresFrontend.Components.Infra.Utils
{
    using System.Diagnostics.CodeAnalysis;

    public static class Assert
    {
        public static void NotNull( [NotNull]object? obj, string message)
        {
            if (obj == null)
            {
                throw new NullReferenceException(message);
            }
        }

        public static void That(bool condition, string message)
        {
            if (!condition)
            {
                throw new Exception(message);
            }
        }
    }
}
