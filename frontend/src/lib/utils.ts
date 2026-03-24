export const getStatusSeverity = (status: string) => {
  switch (status.toLowerCase()) {
    case "running":
      return "success";
    case "queued":
      return "info";
    case "completed":
      return "success";
    case "failed":
      return "danger";
    default:
      return "warning";
  }
};

export const formatDateTime = (dateString: string | Date | undefined) => {
  try {
    if (!dateString) {
      return "Invalid date";
    }
    const date = new Date(dateString);
    console.log(navigator.language)
    return new Intl.DateTimeFormat(navigator.language, {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    }).format(date);
  } catch (e) {
    return "Invalid date";
  }
};

export const isJobStarted = (status: string) => {
  switch (status.toLowerCase()) {
    case "running":
      return true;
    case "queued":
      return false;
    case "completed":
      return true;
    case "cancelled":
      return true;
    case "failed":
      return true;
    default:
      return true;
  }
};

export const isJobFinished = (status: string) => {
  switch (status.toLowerCase()) {
    case "running":
      return false;
    case "queued":
      return false;
    case "completed":
      return true;
    case "cancelled":
      return true;
    case "failed":
      return true;
    default:
      return true;
  }
};


export function formatSecondsToHMS(totalSeconds: number): string {
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  return [
    hours.toString().padStart(2, '0'),
    minutes.toString().padStart(2, '0'),
    seconds.toString().padStart(2, '0')
  ].join(':');
}