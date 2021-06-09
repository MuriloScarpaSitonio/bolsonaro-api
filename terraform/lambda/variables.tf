variable "project_name" {
  description = "The name of the project"
  type        = string
}

variable "function_name" {
  description = "The lambda function name"
  type        = string
}

variable "runtime" {
  description = "The lambda function runtime"
  type        = string
  default     = "python3.8"
}

variable "log_retention" {
  description = "The log retention period in days"
  type        = string
  default     = 7
}

variable "source_dir" {
  description = "The lambda function source directory"
  type        = string
}

variable "memory_size" {
  description = "The memory configuration of the lambda function"
  type        = number
  default     = 128
}

variable "timeout" {
  description = "The lambda function timeout in seconds"
  type        = number
  default     = 15
}

variable "handler" {
  description = "The lambda function entrypoint"
  type        = string
}

variable "env_vars" {
  description = "Environment variables passed to the lambda function"
  type        = map
}